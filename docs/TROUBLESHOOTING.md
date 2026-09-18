# Troubleshooting

- **Frontend cannot reach API**: verify `VITE_API_BASE_URL` and backend port 8000.
- **Upload rejected**: verify extension and file size within configured limits.
- **Task stuck in created state**: ensure backend event loop is running and no runtime errors in logs.
- **PDF extraction placeholder returned**: install PyMuPDF in backend environment.
- **Offline status endpoint not reachable**: verify backend container/service health.
