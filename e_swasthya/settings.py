# Blockchain Configuration
BLOCKCHAIN_CONFIG = {
    'PROVIDER_URL': 'http://127.0.0.1:7545',  # Ganache RPC URL
    'CONTRACT_ADDRESS': '',  # Will be filled after deployment
    'PRIVATE_KEY': '9bdcabc4c6eeeff7f58eed9465ce7cf7602228b4ec468e8e64eef809fc3cd7d4',  # Your Ganache account private key
}

# Add build directory to static files
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'build', 'contracts'),
] 