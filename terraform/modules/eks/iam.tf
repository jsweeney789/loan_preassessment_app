data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

# ── Cluster Role ──────────────────────────────────────────────────────────────
# Assumed by the EKS control plane to manage EC2, ELB, and autoscaling on your behalf

resource "aws_iam_role" "cluster_role" {
  name = "${var.environment}-eks-cluster-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "eks.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })

  tags = merge(var.tags, { Environment = var.environment })
}

# Inline equivalent of AmazonEKSClusterPolicy — avoids iam:AttachRolePolicy
resource "aws_iam_role_policy" "cluster_role" {
  name = "${var.environment}-eks-cluster-policy"
  role = aws_iam_role.cluster_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "EC2Networking"
        Effect = "Allow"
        Action = [
          "ec2:CreateSecurityGroup", "ec2:DeleteSecurityGroup",
          "ec2:AuthorizeSecurityGroupIngress", "ec2:RevokeSecurityGroupIngress",
          "ec2:AuthorizeSecurityGroupEgress", "ec2:RevokeSecurityGroupEgress",
          "ec2:DescribeInstances", "ec2:DescribeRouteTables",
          "ec2:DescribeSecurityGroups", "ec2:DescribeSubnets",
          "ec2:DescribeVpcs", "ec2:DescribeNetworkInterfaces",
          "ec2:DescribeAvailabilityZones", "ec2:DescribeInternetGateways",
          "ec2:DescribeDhcpOptions", "ec2:CreateTags", "ec2:DeleteTags",
          "ec2:DescribeTags"
        ]
        Resource = "*"
      },
      {
        Sid    = "LoadBalancing"
        Effect = "Allow"
        Action = ["elasticloadbalancing:*"]
        Resource = "*"
      },
      {
        Sid    = "AutoScaling"
        Effect = "Allow"
        Action = [
          "autoscaling:DescribeAutoScalingGroups",
          "autoscaling:UpdateAutoScalingGroup",
          "autoscaling:DescribeLaunchConfigurations",
          "autoscaling:DescribeScalingActivities"
        ]
        Resource = "*"
      },
      {
        Sid    = "CloudWatchLogs"
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup", "logs:CreateLogStream",
          "logs:DescribeLogGroups", "logs:PutLogEvents"
        ]
        Resource = "*"
      },
      {
        Sid      = "ServiceLinkedRole"
        Effect   = "Allow"
        Action   = ["iam:CreateServiceLinkedRole"]
        Resource = "*"
        Condition = {
          StringLike = {
            "iam:AWSServiceName" = "elasticloadbalancing.amazonaws.com"
          }
        }
      }
    ]
  })
}

# ── Node Role ─────────────────────────────────────────────────────────────────
# Assumed by EC2 worker nodes — needs ECR pull, CNI networking, and EKS worker permissions

resource "aws_iam_role" "node_role" {
  name = "${var.environment}-eks-node-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "ec2.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })

  tags = merge(var.tags, { Environment = var.environment })
}

# Inline equivalent of AmazonEKSWorkerNodePolicy + AmazonEKS_CNI_Policy + AmazonEC2ContainerRegistryReadOnly
resource "aws_iam_role_policy" "node_role" {
  name = "${var.environment}-eks-node-policy"
  role = aws_iam_role.node_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "EKSWorker"
        Effect = "Allow"
        Action = [
          "ec2:DescribeInstances", "ec2:DescribeRegions",
          "ec2:DescribeRouteTables", "ec2:DescribeSecurityGroups",
          "ec2:DescribeSubnets", "ec2:DescribeVolumes",
          "ec2:DescribeVolumesModifications", "ec2:DescribeVpcs",
          "ec2:DescribeNetworkInterfaces", "ec2:CreateNetworkInterface",
          "ec2:DeleteNetworkInterface", "ec2:AttachNetworkInterface",
          "ec2:ModifyNetworkInterfaceAttribute", "ec2:AssignPrivateIpAddresses",
          "ec2:UnassignPrivateIpAddresses", "ec2:CreateTags"
        ]
        Resource = "*"
      },
      {
        Sid    = "ECRPull"
        Effect = "Allow"
        Action = [
          "ecr:GetAuthorizationToken",
          "ecr:BatchCheckLayerAvailability",
          "ecr:GetDownloadUrlForLayer",
          "ecr:BatchGetImage"
        ]
        Resource = "*"
      },
      {
        Sid    = "SSMParams"
        Effect = "Allow"
        Action = [
          "ssm:GetParameter",
          "ssm:GetParameters",
          "ssm:GetParametersByPath"
        ]
        Resource = "arn:aws:ssm:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:parameter/aws/service/eks/*"
      },
      {
        Sid      = "CloudWatchLogs"
        Effect   = "Allow"
        Action   = ["logs:CreateLogStream", "logs:PutLogEvents", "logs:DescribeLogStreams"]
        Resource = "arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:log-group:/aws/eks/*"
      }
    ]
  })
}

# ── OIDC Provider ─────────────────────────────────────────────────────────────
# Enables IRSA (IAM Roles for Service Accounts) — pods can assume IAM roles
# without node-level credentials

resource "aws_iam_openid_connect_provider" "eks" {
  url             = aws_eks_cluster.eks.identity[0].oidc[0].issuer
  client_id_list  = ["sts.amazonaws.com"]

  # AWS manages OIDC cert rotation for EKS — this thumbprint is the known root CA value
  thumbprint_list = ["9e99a48a9960b14926bb7f3b02e22da2b0ab7280"]

  tags = merge(var.tags, { Environment = var.environment })
}

# ── Cluster Admin Access Entry ─────────────────────────────────────────────────
# Grants the specified IAM role kubectl cluster-admin access via EKS access entries
# (requires authentication_mode = API_AND_CONFIG_MAP on the cluster)

resource "aws_eks_access_entry" "admin" {
  cluster_name  = aws_eks_cluster.eks.name
  principal_arn = var.cluster_admin_role_arn
  type          = "STANDARD"

  tags = merge(var.tags, { Environment = var.environment })
}

resource "aws_eks_access_policy_association" "admin" {
  cluster_name  = aws_eks_cluster.eks.name
  principal_arn = var.cluster_admin_role_arn
  policy_arn    = "arn:aws:eks::aws:cluster-access-policy/AmazonEKSClusterAdminPolicy"

  access_scope {
    type = "cluster"
  }

  depends_on = [aws_eks_access_entry.admin]
}
