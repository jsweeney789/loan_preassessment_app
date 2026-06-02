resource "aws_eks_cluster" "eks" {
  name     = "${var.environment}-eks-cluster"
  role_arn = aws_iam_role.cluster_role.arn

  vpc_config {
    subnet_ids              = var.private_subnet_ids
    endpoint_private_access = true
    endpoint_public_access  = true  # allows kubectl from your laptop; lock down in prod
  }

  # Capture control-plane logs in CloudWatch
  enabled_cluster_log_types = ["api", "audit", "authenticator"]

  depends_on = [aws_iam_role_policy.cluster_role]

  tags = merge(var.tags, {
    Name        = "${var.environment}-eks-cluster"
    Environment = var.environment
  })
}

resource "aws_eks_node_group" "eks" {
  cluster_name    = aws_eks_cluster.eks.name
  node_group_name = "${var.environment}-eks-nodes"
  node_role_arn   = aws_iam_role.node_role.arn
  subnet_ids      = var.private_subnet_ids

  instance_types = [var.node_instance_type]

  scaling_config {
    desired_size = var.desired_nodes
    max_size     = var.max_nodes
    min_size     = var.min_nodes
  }

  # Rolling updates — replace one node at a time
  update_config {
    max_unavailable = 1
  }

  depends_on = [aws_iam_role_policy.node_role]

  tags = merge(var.tags, {
    Name        = "${var.environment}-eks-nodes"
    Environment = var.environment
  })
}
