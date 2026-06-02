output "cluster_name" {
  description = "EKS cluster name — pass to aws eks update-kubeconfig"
  value       = aws_eks_cluster.eks.name
}

output "cluster_endpoint" {
  description = "Kubernetes API server endpoint"
  value       = aws_eks_cluster.eks.endpoint
}

output "cluster_certificate_authority" {
  description = "Base64-encoded CA certificate for the cluster"
  value       = aws_eks_cluster.eks.certificate_authority[0].data
  sensitive   = true
}

output "oidc_provider_arn" {
  description = "OIDC provider ARN — used when creating IRSA roles for pods"
  value       = aws_iam_openid_connect_provider.eks.arn
}

output "oidc_provider_url" {
  description = "OIDC provider URL — used in the trust policy of IRSA roles"
  value       = aws_iam_openid_connect_provider.eks.url
}

output "node_role_arn" {
  description = "ARN of the node IAM role"
  value       = aws_iam_role.node_role.arn
}
