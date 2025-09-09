# ERPNext Country Specific Functionality for República Dominicana (CSF_RD)

## _*Enhancing ERPNext with Dominican Republic-specific features for tax compliance, electronic invoicing, and localized business needs.*_

## Overview

This is a custom application designed to extend the capabilities of [ERPNext](https://erpnext.com/) to meet the unique regulatory and operational requirements of businesses in the Dominican Republic. This app provides seamless integration with DGII (Dirección General de Impuestos Internos) systems, electronic invoicing (eCF), and additional tools tailored to streamline business processes.

Key features include:

- Electronic invoicing (eCF) compliance with DGII regulations.
- Integration with DGII APIs through Node.js server.
- Comprehensive tax reporting for Dominican Republic.
- Localized financial and tax reporting.
- RNC validation and NCF management.

This README provides an overview of the application, its features, installation instructions, and additional resources to get you started.

---

## Features

### 1. Electronic Invoicing (eCF)

Designed to ensure compliance with Dominican Republic electronic invoicing regulations, these features generate the necessary documentation for fiscal compliance.

- **eCF Document Management**  
  Manages electronic fiscal documents (eCF) with DGII integration
- **NCF (Número de Comprobante Fiscal) Management**  
  Handles fiscal document numbering according to DGII standards
- **RNC Validation**  
  Validates RNC (Registro Nacional de Contribuyentes) format and authenticity
- **QR Code Generation**  
  Generates QR codes for electronic invoices as required by DGII

### 2. Tax Reports

Streamlined reporting for sales and purchase taxes to ensure compliance with Dominican Republic tax laws.

- **DGII Tax Report**  
  Summarizes VAT and other taxes for DGII reporting
- **eCF Summary Report**  
  Provides overview of all electronic fiscal documents sent to DGII

### 3. Tax Compliance Features

Custom fields and integrations to meet DGII tax regulations and facilitate seamless reporting.

- **Custom RNC Fields**  
  Captures RNC information in Customer and Supplier records
- **NCF Configuration**  
  Manages fiscal document number sequences
- **DGII Customer Directory**  
  Maintains directory of authorized customers for electronic invoicing

### 4. Node.js Integration Server

- **DGII API Integration**  
  Node.js server that handles communication with DGII APIs
- **Certificate Management**  
  Manages digital certificates for electronic document signing
- **Document Processing**  
  Processes and signs electronic documents before sending to DGII

---

## Installation 🛠️

Follow the instructions below to install CSF_RD on your ERPNext instance.

### Prerequisites

- A working ERPNext instance (v13 or higher recommended).
- Access to a terminal with `bench` commands enabled (for self-hosting).
- Git installed on your system.
- Node.js server running (see Node.js Server Setup below).

### Option 1: Manual Installation (Self-Hosting)

1. **Set Up Frappe Bench**  
   If you don't already have a Frappe Bench instance, follow the [official Frappe installation guide](https://frappeframework.com/docs/user/en/installation) to set it up.

2. **Add the CSF_RD App**  
   In your Bench directory, run the following command to download the app from GitHub:

   ```sh
   bench get-app https://github.com/your-org/csf_rd.git
   ```

3. **Install the App on Your Site**
   Replace `<your.site.name.here>` with your ERPNext site name and run:

   ```sh
   bench --site <your.site.name.here> install-app csf_rd
   ```

4. **Set Up Node.js Server**
   Follow the Node.js Server Setup instructions below.

5. **Verify Installation**

   Restart your Bench instance and log in to ERPNext to confirm that the `CSF_RD` app appears in your app list.

---

### Node.js Server Setup

1. **Navigate to the Node.js server directory**
   ```sh
   cd dgii-server
   ```

2. **Install dependencies**
   ```sh
   npm install
   ```

3. **Configure environment**
   ```sh
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Start the server**
   ```sh
   npm start
   # or for development
   npm run dev
   ```

---

## Configuration

After installation, configure the app to suit your business needs:

1. **Set Up DGII Settings**
   - Configure your DGII certificate and credentials
   - Set up the Node.js server URL
   - Configure environment (test/cert/production)

2. **Configure NCF Sequences**
   - Set up fiscal document number sequences
   - Configure different NCF types (A, B, C, etc.)

3. **Test Integration**
   - Test connection with DGII
   - Verify certificate validation
   - Test electronic document sending

---

## Usage Examples

### Sending an Electronic Invoice

1. Create a Sales Invoice in ERPNext
2. Enter customer RNC in the Tax ID field
3. Submit the invoice
4. The system automatically creates an eCF Document
5. The invoice is sent to DGII automatically

### Generating Tax Reports

1. Navigate to the **República Dominicana** module in ERPNext
2. Select **DGII Tax Report** from the reports
3. Choose the **company** and **date range**
4. Export the report as a **PDF** for DGII submission

---

## Architecture

```
ERPNext (Python/Frappe) ←→ Node.js Server ←→ DGII APIs
     ↓                        ↓
  CSF_RD App              DGII-eCF Library
```

The application uses a hybrid architecture where:
- ERPNext handles business logic and data management
- Node.js server manages DGII API communication
- DGII-eCF library handles electronic document processing

---

## Authors

- CSF RD Team

## 🔗 Links

- [DGII Official Documentation](https://dgii.gov.do/)
- [ERPNext Documentation](https://docs.erpnext.com/)

## Related

For more technical documentation related with Electronic Invoicing:

- [DGII official documentation (Facturación Electrónica)](https://dgii.gov.do/cicloContribuyente/facturacion/comprobantesFiscalesElectronicosE-CF/Paginas/default.aspx)
- [DGII Technical Doc](https://dgii.gov.do/cicloContribuyente/facturacion/comprobantesFiscalesElectronicosE-CF/Paginas/documentacionSobreE-CF.aspx)
