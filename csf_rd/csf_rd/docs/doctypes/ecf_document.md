# eCF Document

## Overview

The eCF Document doctype manages electronic fiscal documents (eCF) for the Dominican Republic's electronic invoicing system.

## Fields

### Document Information
- **Company**: The company issuing the document
- **Sales Invoice**: Link to the original sales invoice
- **NCF**: Número de Comprobante Fiscal (Fiscal Document Number)
- **RNC Emisor**: Issuer's RNC
- **RNC Comprador**: Buyer's RNC
- **Fecha Emisión**: Issue date
- **Monto Total**: Total amount

### DGII Integration
- **Status**: Current status in DGII (Draft/Sent/Accepted/Rejected/Error)
- **Track ID**: DGII tracking ID
- **DGII Response**: Raw response from DGII
- **QR Code URL**: URL for the QR code

### Security
- **Código Seguridad**: Security code for the document

## Workflow

1. **Creation**: Automatically created when a Sales Invoice is submitted
2. **Preparation**: Document data is prepared for DGII format
3. **Sending**: Document is sent to DGII via Node.js server
4. **Tracking**: Status is tracked using Track ID
5. **Completion**: Final status is recorded

## Actions

- **Send to DGII**: Manually send document to DGII
- **Check Status**: Check current status in DGII
- **Generate QR Code**: Generate QR code for the document

## Integration

- Automatically triggered on Sales Invoice submission
- Integrates with DGII Settings for configuration
- Uses Node.js server for DGII communication
