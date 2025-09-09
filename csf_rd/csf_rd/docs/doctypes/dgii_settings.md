# DGII Settings

## Overview

The DGII Settings doctype is used to configure the connection and authentication with the Dominican Republic's tax authority (DGII) for electronic invoicing.

## Fields

### Basic Configuration
- **Company**: The company for which these settings apply
- **Environment**: The DGII environment (Test/Cert/Production)
- **DGII Server URL**: URL of the Node.js server that handles DGII communication

### Certificate Configuration
- **Certificate File (.p12)**: Digital certificate file for DGII authentication
- **Certificate Content (Base64)**: Base64 encoded certificate content
- **Certificate Password**: Password for the certificate
- **Company RNC**: Company's RNC (Registro Nacional de Contribuyentes)
- **Company Name**: Company's legal name

### API Configuration
- **API Key**: API key for additional authentication
- **API Secret**: API secret for additional authentication
- **Timeout**: Request timeout in seconds
- **Retry Attempts**: Number of retry attempts for failed requests

## Usage

1. Create a new DGII Settings record
2. Configure the certificate and company information
3. Test the connection using the "Test Connection" button
4. Save the settings

## Security Notes

- Certificate passwords are stored securely
- API secrets are encrypted
- Test connection validates credentials without storing them
