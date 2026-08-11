variable "webhook_url" {
  description = "Webhook URL for notifications"
  type        = string
  sensitive   = true
  default     = "https://dummy.webhook.url"
}