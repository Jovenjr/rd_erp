# DGII Integration

## Overview

The DGII Integration feature provides seamless integration with the Dominican Republic's tax authority (DGII) for electronic invoicing compliance.

## Components

### 1. Node.js Server
- Handles communication with DGII APIs
- Manages digital certificate authentication
- Processes electronic document signing
- Provides REST API endpoints for ERPNext

### 2. ERPNext Integration
- Automatic eCF document creation
- Real-time status tracking
- QR code generation
- Tax reporting

### 3. Certificate Management
- Digital certificate validation
- Secure certificate storage
- Environment-specific configuration

## Setup Process

### 1. Configure DGII Settings
1. Navigate to **CSF RD > DGII Settings**
2. Create a new record
3. Upload your digital certificate (.p12 file)
4. Enter certificate password
5. Configure company RNC and name
6. Set DGII server URL
7. Test connection

### 2. Configure NCF Sequences
1. Navigate to **CSF RD > NCF Configuration**
2. Create sequences for different NCF types:
   - **A**: Factura de Crédito Fiscal
   - **B**: Factura de Consumo
   - **C**: Nota de Débito
   - **D**: Nota de Crédito

### 3. Start Node.js Server
1. Navigate to `dgii-server` directory
2. Install dependencies: `npm install`
3. Configure environment: `cp .env.example .env`
4. Start server: `npm start`

## Usage

### Automatic eCF Creation
When a Sales Invoice is submitted:
1. System checks if customer has RNC
2. Creates eCF Document automatically
3. Generates NCF using configured sequences
4. Sends document to DGII
5. Tracks status and updates accordingly

### Manual Operations
- **Send to DGII**: Manually send any eCF document
- **Check Status**: Verify current status in DGII
- **Generate QR Code**: Create QR code for printing

## Environments

### Test Environment (TesteCF)
- Used for development and testing
- No real tax impact
- Full functionality testing

### Certification Environment (CerteCF)
- Used for certification process
- Limited functionality
- Pre-production testing

### Production Environment (eCF)
- Live production environment
- Real tax documents
- Full compliance required

## Troubleshooting

### Common Issues
1. **Certificate Errors**: Verify certificate validity and password
2. **Connection Errors**: Check DGII server URL and status
3. **NCF Errors**: Verify NCF configuration and sequences
4. **Status Errors**: Check DGII response and retry if needed

### Support
For technical support, contact the development team or create an issue in the repository.
