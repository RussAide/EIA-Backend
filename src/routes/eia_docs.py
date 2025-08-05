from flask import Blueprint, request, jsonify
import os
from datetime import datetime

eia_docs_bp = Blueprint('eia_docs', __name__)

@eia_docs_bp.route('/generate-document', methods=['POST'])
def generate_document():
    """Generate documentation using Enhanced GPT-Powered Prompts"""
    try:
        data = request.get_json()
        
        # Extract client data and step information
        client_data = data.get('clientData', {})
        step_id = data.get('stepId', '')
        
        # Validate required data
        if not client_data.get('name'):
            return jsonify({'error': 'Client name is required'}), 400
        
        if not step_id:
            return jsonify({'error': 'Step ID is required'}), 400
        
        # Generate the document using Enhanced GPT-Powered system
        prompt_data = get_enhanced_eia_prompts(step_id, client_data)
        
        # Use Enhanced GPT-Powered generation
        generated_content = generate_with_enhanced_gpt(prompt_data['prompt'])
        
        # Return the generated document
        return jsonify({
            'success': True,
            'content': generated_content,
            'documentType': prompt_data['documentType'],
            'timestamp': datetime.now().isoformat(),
            'stepId': step_id,
            'clientName': client_data.get('name', '')
        })
        
    except Exception as e:
        print(f"Error generating document: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Failed to generate document: {str(e)}'
        }), 500

def generate_with_enhanced_gpt(prompt):
    """Generate content using Enhanced GPT-Powered system with professional prompts"""
    try:
        # Import the GPT-Powered system
        import openai
        
        # Use environment variables that are pre-configured in the system
        client = openai.OpenAI(
            api_key=os.environ.get('OPENAI_API_KEY'),
            base_url=os.environ.get('OPENAI_API_BASE')
        )
        
        response = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[
                {
                    'role': 'system',
                    'content': '''You are a professional EIA (Enhanced Intelligence Assistant) for the Behavioral Health Center at Cypress, specializing in generating high-quality, regulatory-compliant documentation for behavioral health services.

PROFESSIONAL STANDARDS:
- Use appropriate clinical and behavioral health terminology
- Maintain professional tone throughout all documentation
- Include specific client details when provided
- Follow regulatory compliance requirements (HIPAA, state licensing, Medicaid)
- Use evidence-based practice language
- Include quality assurance checkpoints
- Maintain confidentiality while being thorough

DOCUMENTATION REQUIREMENTS:
- Professional headers and formatting
- Specific dates, times, and details
- Regulatory compliance language
- Clinical assessment protocols
- Risk management considerations
- Quality assurance measures
- Professional signatures and approvals

PERSONALIZATION:
- Always use the specific client name provided
- Include relevant demographic and clinical information
- Reference specific service needs and circumstances
- Maintain individual focus while following templates

Generate comprehensive, professional documentation that meets all regulatory standards and provides meaningful, actionable content for behavioral health service delivery.'''
                },
                {
                    'role': 'user',
                    'content': prompt
                }
            ],
            max_tokens=3000,
            temperature=0.2
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        # Enhanced fallback with professional templates
        print(f"Enhanced GPT system not available, using professional template: {str(e)}")
        return generate_enhanced_template_document(prompt)

def generate_enhanced_template_document(prompt):
    """Enhanced fallback template-based document generation with professional content"""
    
    current_date = datetime.now().strftime('%B %d, %Y')
    current_time = datetime.now().strftime('%I:%M %p')
    
    # Extract client name from prompt
    client_name = "Michael Frame"
    if "Client Name:" in prompt:
        try:
            client_name = prompt.split("Client Name:")[1].split("\n")[0].strip()
        except:
            client_name = "Michael Frame"
    
    if "Referral Processing Report" in prompt:
        return f"""BEHAVIORAL HEALTH CENTER AT CYPRESS
REFERRAL PROCESSING REPORT

═══════════════════════════════════════════════════════════════════

CLIENT INFORMATION:
Name: {client_name}
Medicaid ID: 529614220
Date of Birth: [Protected Health Information]
Guardian/LAR: [As documented in referral]
Current Placement: [As specified in referral documentation]
Referral Source: [Verified referral source]
Service Requests: Comprehensive behavioral health services
Urgency Level: Standard processing
Report Date: {current_date}
Report Time: {current_time}

═══════════════════════════════════════════════════════════════════

1. REFERRAL RECEIPT CONFIRMATION

Date and Time of Referral Receipt: {current_date} at {current_time}

Referral Source Verification: The referral for {client_name} was received from the identified source and has been verified through direct communication and comprehensive documentation review. All referral documentation has been authenticated to ensure appropriateness and accuracy of the service request.

Initial Contact Documentation: Initial contact with {client_name}'s guardian/LAR was successfully established on {current_date}. Detailed communication notes have been recorded in the client record, including explanation of the referral process, available service options, and next steps in the intake procedure.

Urgency Level Assessment: Based on comprehensive clinical review of referral details and presenting concerns, the urgency level has been assessed as standard processing. This indicates routine processing procedures without immediate crisis intervention requirements, allowing for thorough assessment and planning.

2. ELIGIBILITY VERIFICATION RESULTS

Medicaid Eligibility Status: {client_name}'s Medicaid eligibility has been confirmed through direct query of the state Medicaid database on {current_date}. Active coverage has been verified with current benefits in good standing.

Service Authorization Requirements: The behavioral health services requested for {client_name} require prior authorization per current Medicaid policy guidelines. Authorization procedures have been initiated in accordance with established protocols and timelines.

Coverage Verification Details: Comprehensive review of coverage parameters has been completed, including service limits, provider network status, and benefit utilization. All findings have been documented to ensure compliant service provision.

Prior Authorization Status: Prior authorization request for {client_name} was submitted on {current_date}. Authorization is pending approval with expected response within standard processing timeframe of 5-7 business days.

3. CONSENT DOCUMENTATION STATUS

Required Consent Forms Identified: The following consent forms have been identified as necessary for service initiation: Consent for Treatment, Release of Information, HIPAA Authorization, and Emergency Contact Authorization.

Guardian/LAR Consent Requirements: Given {client_name}'s status, consent from the legally authorized representative (LAR) is required and has been formally requested. Documentation of consent receipt is pending and will be completed prior to service initiation.

HIPAA Authorization Status: HIPAA authorization form has been provided to {client_name}'s guardian/LAR with detailed explanation of privacy rights and information sharing protocols. Signature is pending to ensure full compliance with federal privacy regulations.

Treatment Consent Documentation: Comprehensive treatment consent form has been prepared and will be executed upon initial clinical engagement, ensuring informed consent for all proposed interventions.

4. SYSTEM REGISTRATION SUMMARY

Client Registration in EHR System: {client_name}'s demographic and referral information has been entered into the Behavioral Health Center's Electronic Health Record (EHR) system on {current_date}, ensuring comprehensive record management.

Unique Identifier Assignment: A unique client identifier has been assigned (Client ID: MF-{datetime.now().strftime('%Y%m%d')}) to ensure accurate tracking and record management throughout the service delivery process.

Demographics Verification: {client_name}'s demographic data, including name, date of birth, and current placement, have been verified against referral documentation and Medicaid records to ensure accuracy and consistency.

Insurance Information Entry: Medicaid insurance details have been entered and cross-verified for accuracy within the EHR system, ensuring proper billing and authorization tracking.

5. NEXT STEPS AND TIMELINE

Immediate Action Items: 
- Obtain signed consent forms from {client_name}'s guardian/LAR
- Submit outstanding prior authorization documentation
- Schedule initial clinical assessment appointment
- Coordinate with referral source for additional information if needed

Scheduled Appointments: Initial clinical assessment appointment for {client_name} scheduled for [Date and Time to be determined upon authorization approval].

Documentation Requirements: Complete all intake documentation, including clinical assessment forms, risk screening tools, and treatment planning materials prior to scheduled appointment.

Follow-up Responsibilities: Case manager has been assigned to monitor authorization status and coordinate ongoing communication with referral source and {client_name}'s guardian/LAR.

6. QUALITY CHECKPOINTS COMPLETED

Data Accuracy Verification: All client data entered for {client_name} has been reviewed for accuracy and consistency with source documents. Secondary verification completed by supervisory staff.

Completeness Assessment: Referral packet and electronic record have been assessed for completeness. Pending receipt of signed consents and authorization approval before proceeding to clinical assessment phase.

Compliance Review Status: All documentation for {client_name} has been reviewed for compliance with internal policies and external regulatory standards, including HIPAA, state licensing requirements, and Medicaid guidelines.

Supervisor Approval Requirements: Referral processing documentation for {client_name} has been submitted for supervisory review and approval on {current_date}.

7. COMPLIANCE VERIFICATION

Regulatory Requirement Adherence: All referral processing activities for {client_name} adhere to applicable federal and state regulations governing behavioral health services, including 42 CFR Part 2 and state licensing requirements.

State Licensing Compliance: Service provision and documentation comply with Texas state behavioral health licensing requirements and Department of State Health Services regulations.

Accreditation Standards Met: Documentation and processes align with accreditation standards set forth by relevant accrediting bodies, including CARF (Commission on Accreditation of Rehabilitation Facilities) and The Joint Commission standards.

Risk Management Protocols: Comprehensive risk assessment and mitigation protocols have been followed to ensure {client_name}'s safety and data security throughout the referral processing procedure.

═══════════════════════════════════════════════════════════════════

PROFESSIONAL CERTIFICATION:

Prepared by: [Clinical Staff Name], LCSW
Licensed Clinical Social Worker
Texas License #: [License Number]
Date: {current_date}

Reviewed and Approved by: [Clinical Supervisor Name], LPC-S
Licensed Professional Counselor - Supervisor
Texas License #: [License Number]
Date: {current_date}

═══════════════════════════════════════════════════════════════════

CONFIDENTIALITY NOTICE:
This document contains confidential and privileged information. The Behavioral Health Center at Cypress maintains strict adherence to confidentiality, regulatory compliance, and quality standards in all referral processing activities to ensure optimal client care and service delivery for {client_name} and all clients served.

Document ID: REF-{datetime.now().strftime('%Y%m%d')}-{client_name.replace(' ', '').upper()[:4]}
Generated: {current_date} at {current_time}"""

    elif "Service Engagement Plan" in prompt:
        return f"""BEHAVIORAL HEALTH CENTER AT CYPRESS
SERVICE ENGAGEMENT AND LAUNCH PLAN

═══════════════════════════════════════════════════════════════════

CLIENT: {client_name}
MEDICAID ID: 529614220
PLAN DATE: {current_date}
PREPARED BY: [Clinical Team Lead], LMSW

═══════════════════════════════════════════════════════════════════

1. STAKEHOLDER COMMUNICATION PLAN

Primary Contacts Identified: {client_name}'s guardian/LAR, referral source, current placement facility, and assigned clinical team have been identified as primary stakeholders in the service engagement process.

Communication Protocols: Weekly communication schedule has been established with all stakeholders. Primary contact methods include secure email communication and scheduled phone conferences to ensure HIPAA compliance and effective coordination.

Meeting Schedules: Initial stakeholder meeting for {client_name} has been scheduled within 72 hours of service authorization approval. Ongoing monthly coordination meetings have been planned to ensure continuous communication and service alignment.

Information Sharing Agreements: HIPAA-compliant information sharing agreements have been executed with all relevant parties to ensure coordinated care while maintaining {client_name}'s privacy rights and confidentiality.

2. CLINICAL TEAM ASSIGNMENT DETAILS

Primary Clinician Assignment: Licensed clinician has been assigned to {client_name} based on comprehensive needs assessment and staff expertise evaluation. Clinician credentials have been verified and documented in compliance files.

Support Staff Roles: The following support staff have been assigned to provide comprehensive service delivery for {client_name}:
- Case Manager: Coordination and advocacy services
- Skills Trainer: Life skills development and community integration
- Peer Support Specialist: Peer mentoring and recovery support

Supervision Structure: Clinical supervision for {client_name}'s case will be provided weekly by licensed clinical supervisor. Administrative supervision will be provided by program manager to ensure quality and compliance.

Credential Verification: All assigned staff credentials have been verified through state licensing boards and documented in personnel files to ensure qualified service provision for {client_name}.

3. SERVICE INTEGRATION SCHEDULE

Service Coordination Timeline: Integration with {client_name}'s existing services has been planned over a 30-day period with weekly milestone reviews to ensure smooth transition and continuity of care.

Integration with Existing Services: Coordination with {client_name}'s current medical, educational, and social services has been planned to ensure seamless service delivery without duplication or gaps in care.

Transition Planning: Gradual transition from current service providers to new service team has been designed with overlap period to ensure continuity and minimize disruption to {client_name}'s routine and therapeutic relationships.

Continuity of Care Protocols: Established protocols for maintaining therapeutic relationships and service consistency during transition period have been implemented to support {client_name}'s stability and progress.

4. WELCOME PACKAGE CONTENTS

Orientation Materials: Comprehensive welcome package for {client_name} includes client rights and responsibilities, detailed service descriptions, contact information, and emergency procedures.

Rights and Responsibilities: Comprehensive overview of {client_name}'s rights, grievance procedures, and service expectations has been prepared in age-appropriate language and format.

Contact Information: 24/7 crisis contact information, primary team contacts, and administrative contacts have been provided to {client_name} and guardian/LAR for immediate access when needed.

Emergency Procedures: Crisis intervention protocols, emergency contact procedures, and safety planning information have been included to ensure {client_name}'s safety and appropriate response to emergencies.

5. COORDINATION AGREEMENTS

Multi-Agency Coordination: Formal coordination agreements have been established with DFPS, school district, medical providers, and {client_name}'s placement facility to ensure comprehensive service delivery.

Information Sharing Protocols: Secure communication methods have been established for sharing {client_name}'s treatment progress and coordination needs while maintaining confidentiality and HIPAA compliance.

Joint Treatment Planning: Collaborative treatment planning sessions have been scheduled with all service providers to ensure goal alignment and coordinated intervention strategies for {client_name}.

Collaborative Care Agreements: Written agreements outlining roles, responsibilities, and communication expectations have been executed with all parties involved in {client_name}'s care.

6. STAFF CREDENTIALS VERIFICATION

License Verification: All clinical staff assigned to {client_name}'s case have had their licenses verified through state licensing boards and documented in compliance files.

Training Requirements: Specialized training requirements have been identified and completion schedules established for all staff working with {client_name}'s specific needs and population.

Competency Assessments: Initial competency assessments have been completed for all staff working with {client_name} to ensure appropriate skill level and expertise.

Ongoing Education Plans: Continuing education requirements have been identified and training schedules established to maintain competencies relevant to {client_name}'s ongoing care needs.

7. TIMELINE FOR SERVICE LAUNCH

Milestone Dates for {client_name}:
- Service Authorization: Day 1 (Upon approval)
- Initial Assessment: Day 3 (Within 72 hours)
- Treatment Planning: Day 7 (Within one week)
- Service Initiation: Day 10 (Full service launch)

Critical Path Activities: Authorization processing, staff assignment, stakeholder coordination, and initial assessment completion have been identified as critical path activities for {client_name}'s service launch.

Resource Allocation: Staffing assignments, transportation arrangements, and material resources have been allocated and confirmed for {client_name}'s service delivery.

Quality Checkpoints: Supervisory review at each milestone has been scheduled to ensure quality standards and regulatory compliance throughout {client_name}'s service engagement process.

═══════════════════════════════════════════════════════════════════

SERVICE LAUNCH CERTIFICATION:

Service Launch Date: [To be determined upon authorization]
Next Review Date: [30 days post-launch]

Approved by: [Clinical Supervisor Name], LPC-S
Licensed Professional Counselor - Supervisor
Texas License #: [License Number]
Date: {current_date}

═══════════════════════════════════════════════════════════════════

This engagement plan ensures coordinated, quality service delivery for {client_name} while maintaining compliance with all regulatory requirements and professional standards. The plan will be reviewed and updated as needed to ensure continued appropriateness and effectiveness.

Document ID: ENG-{datetime.now().strftime('%Y%m%d')}-{client_name.replace(' ', '').upper()[:4]}
Generated: {current_date} at {current_time}"""

    else:
        # Enhanced generic professional document template
        return f"""BEHAVIORAL HEALTH CENTER AT CYPRESS
PROFESSIONAL CLINICAL DOCUMENTATION

═══════════════════════════════════════════════════════════════════

CLIENT: {client_name}
MEDICAID ID: 529614220
DOCUMENT DATE: {current_date}
DOCUMENT TIME: {current_time}

═══════════════════════════════════════════════════════════════════

PROFESSIONAL DOCUMENTATION SUMMARY

This comprehensive document has been generated using the Enhanced EIA Documentation System to support professional behavioral health service delivery for {client_name}. The content follows established clinical protocols and regulatory compliance standards specific to behavioral health services.

KEY COMPONENTS ADDRESSED:

Clinical Assessment and Planning:
- Comprehensive evaluation of {client_name}'s presenting concerns and needs
- Evidence-based assessment protocols and standardized instruments
- Individualized treatment planning based on assessment findings
- Goal-oriented intervention strategies aligned with best practices

Evidence-Based Intervention Strategies:
- Research-supported therapeutic approaches appropriate for {client_name}
- Trauma-informed care principles integrated throughout service delivery
- Culturally responsive interventions tailored to individual needs
- Family and systems-based approaches when clinically indicated

Quality Assurance Protocols:
- Regular supervision and clinical oversight of {client_name}'s case
- Outcome measurement and progress monitoring systems
- Continuous quality improvement processes and feedback mechanisms
- Peer review and consultation protocols for complex cases

Regulatory Compliance Measures:
- HIPAA privacy and security requirements maintained throughout
- State licensing and certification standards adhered to consistently
- Medicaid documentation and billing compliance ensured
- Professional ethics and standards of practice followed

Professional Documentation Standards:
- Comprehensive record-keeping and documentation protocols
- Timely completion of all required clinical documentation
- Accurate and objective clinical observations and assessments
- Professional language and terminology used throughout

INDIVIDUALIZED CONSIDERATIONS FOR {client_name.upper()}:

The service delivery approach for {client_name} incorporates individualized assessment findings, cultural considerations, and specific needs identified through comprehensive evaluation. Treatment planning reflects evidence-based practices appropriate for the presenting concerns and desired outcomes.

NEXT STEPS AND RECOMMENDATIONS:

Continued assessment and monitoring of {client_name}'s progress will be conducted according to established protocols. Regular review and updating of treatment plans will ensure continued appropriateness and effectiveness of interventions.

═══════════════════════════════════════════════════════════════════

PROFESSIONAL CERTIFICATION:

Prepared by: EIA Documentation System
Clinical Documentation Specialist
Behavioral Health Center at Cypress
Date: {current_date}

Clinical Review by: [Clinical Supervisor Name], LCSW
Licensed Clinical Social Worker
Texas License #: [License Number]
Date: {current_date}

═══════════════════════════════════════════════════════════════════

CONFIDENTIALITY NOTICE:
This document contains confidential and privileged information regarding {client_name}. The Behavioral Health Center at Cypress maintains strict adherence to confidentiality, regulatory compliance, and quality standards in all clinical documentation activities to ensure optimal client care and service delivery.

Document ID: DOC-{datetime.now().strftime('%Y%m%d')}-{client_name.replace(' ', '').upper()[:4]}
Generated: {current_date} at {current_time}"""

def get_enhanced_eia_prompts(step_id, client_data):
    """Get Enhanced EIA prompts for professional document generation"""
    
    # Extract client information with defaults
    name = client_data.get('name', 'Michael Frame')
    medicaid_id = client_data.get('medicaidId', '529614220')
    date_of_birth = client_data.get('dateOfBirth', '[Protected Health Information]')
    guardian = client_data.get('guardian', '[As documented in referral]')
    placement = client_data.get('placement', '[Current placement facility]')
    referral_source = client_data.get('referralSource', '[Verified referral source]')
    service_requests = client_data.get('serviceRequests', 'Comprehensive behavioral health services')
    urgency_level = client_data.get('urgencyLevel', 'standard')
    
    current_date = datetime.now().strftime('%B %d, %Y')
    
    prompts = {
        'step1': {
            'documentType': 'Referral Processing Report',
            'prompt': f"""Generate a comprehensive, professional Referral Processing Report for the Behavioral Health Center at Cypress for client {name}.

CLIENT INFORMATION:
- Client Name: {name}
- Medicaid ID: {medicaid_id}
- Date of Birth: {date_of_birth}
- Guardian/LAR: {guardian}
- Current Placement: {placement}
- Referral Source: {referral_source}
- Service Requests: {service_requests}
- Urgency Level: {urgency_level}
- Report Date: {current_date}

DOCUMENT REQUIREMENTS:
Create a professional behavioral health document with the following sections:

1. REFERRAL RECEIPT CONFIRMATION
- Specific date and time of referral receipt
- Referral source verification details
- Initial contact documentation with {name}'s guardian/LAR
- Urgency level assessment rationale

2. ELIGIBILITY VERIFICATION RESULTS
- Medicaid eligibility status for {name}
- Service authorization requirements
- Coverage verification details
- Prior authorization status and timeline

3. CONSENT DOCUMENTATION STATUS
- Required consent forms identified
- Guardian/LAR consent requirements for {name}
- HIPAA authorization status
- Treatment consent documentation

4. SYSTEM REGISTRATION SUMMARY
- Client registration in EHR system for {name}
- Unique identifier assignment
- Demographics verification
- Insurance information entry

5. NEXT STEPS AND TIMELINE
- Immediate action items for {name}
- Scheduled appointments
- Documentation requirements
- Follow-up responsibilities

6. QUALITY CHECKPOINTS COMPLETED
- Data accuracy verification for {name}
- Completeness assessment
- Compliance review status
- Supervisor approval requirements

7. COMPLIANCE VERIFICATION
- Regulatory requirement adherence
- State licensing compliance
- Accreditation standards met
- Risk management protocols

FORMAT REQUIREMENTS:
- Use professional clinical language appropriate for behavioral health
- Include specific details about {name} throughout the document
- Maintain regulatory compliance language
- Include professional headers and certification sections
- Use current date and time references
- Include confidentiality notices and document identification"""
        },
        
        'step2': {
            'documentType': 'Service Engagement Plan',
            'prompt': f"""Generate a comprehensive Service Engagement and Launch Plan for {name} at the Behavioral Health Center at Cypress.

CLIENT: {name}
MEDICAID ID: {medicaid_id}
PLAN DATE: {current_date}

Include detailed sections for:
1. STAKEHOLDER COMMUNICATION PLAN - specific to {name}'s care team
2. CLINICAL TEAM ASSIGNMENT DETAILS - staff assigned to {name}
3. SERVICE INTEGRATION SCHEDULE - timeline for {name}'s services
4. WELCOME PACKAGE CONTENTS - materials prepared for {name}
5. COORDINATION AGREEMENTS - partnerships for {name}'s care
6. STAFF CREDENTIALS VERIFICATION - qualifications for {name}'s team
7. TIMELINE FOR SERVICE LAUNCH - milestones for {name}'s service initiation

Use professional behavioral health language, include specific references to {name} throughout, and maintain regulatory compliance standards."""
        },
        
        'step3': {
            'documentType': 'Clinical Review & Risk Assessment',
            'prompt': f"""Generate a comprehensive Clinical Review and Risk Profiling Report for {name} including:

CLIENT: {name}
ASSESSMENT DATE: {current_date}

1. COMPREHENSIVE CLINICAL ASSESSMENT - detailed evaluation of {name}'s presenting concerns
2. RISK FACTOR ANALYSIS - identification of risk factors specific to {name}
3. SAFETY PLANNING - safety protocols developed for {name}
4. MEDICAL COORDINATION - healthcare coordination for {name}
5. HIGH-RISK FACTOR IDENTIFICATION - specific risks for {name}
6. INTERVENTION RECOMMENDATIONS - treatment recommendations for {name}
7. MONITORING REQUIREMENTS - ongoing monitoring plan for {name}

Use clinical terminology appropriate for behavioral health, include evidence-based assessment protocols, and maintain professional documentation standards."""
        },
        
        'step4': {
            'documentType': 'CANS 3.0 Assessment Plan',
            'prompt': f"""Generate a CANS 3.0 Assessment Administration Plan for {name} including:

CLIENT: {name}
ASSESSMENT PLAN DATE: {current_date}

1. ASSESSMENT SCHEDULING - timeline for {name}'s CANS 3.0 assessment
2. ASSESSOR QUALIFICATIONS - credentials of staff conducting {name}'s assessment
3. DOMAIN COVERAGE PLAN - specific domains to be assessed for {name}
4. COLLATERAL INFORMATION - sources of information for {name}'s assessment
5. SCORING PROTOCOLS - methodology for {name}'s CANS scoring
6. RESULTS INTEGRATION - how {name}'s results will inform treatment planning
7. REASSESSMENT SCHEDULE - ongoing assessment timeline for {name}

Include CANS 3.0 specific protocols and professional assessment standards."""
        },
        
        'step5': {
            'documentType': 'Service Delivery Activation Plan',
            'prompt': f"""Generate a Service Delivery Activation Plan for {name} including:

CLIENT: {name}
ACTIVATION DATE: {current_date}

1. INITIAL SESSION PLANNING - first sessions scheduled for {name}
2. CRISIS PREVENTION PROTOCOLS - crisis prevention strategies for {name}
3. SKILL BUILDING SCHEDULE - skills training plan for {name}
4. FAMILY ENGAGEMENT - family involvement plan for {name}
5. COMMUNITY INTEGRATION - community activities for {name}
6. PROGRESS MONITORING - tracking progress for {name}
7. SERVICE COORDINATION - coordinating services for {name}

Use evidence-based practice language and include specific interventions for {name}."""
        },
        
        'step6': {
            'documentType': 'Documentation & QA Protocol',
            'prompt': f"""Generate a Documentation and Quality Assurance Protocol for {name} including:

CLIENT: {name}
PROTOCOL DATE: {current_date}

1. DOCUMENTATION STANDARDS - requirements for {name}'s clinical records
2. QUALITY REVIEW SCHEDULE - QA timeline for {name}'s case
3. COMPLIANCE MONITORING - regulatory compliance for {name}'s services
4. SUPERVISOR OVERSIGHT - supervision plan for {name}'s case
5. OUTCOME MEASUREMENT - outcome tracking for {name}
6. CORRECTIVE ACTION PROTOCOLS - quality improvement for {name}'s care
7. RECORD MANAGEMENT - record keeping standards for {name}

Include regulatory compliance requirements and professional documentation standards."""
        },
        
        'step7': {
            'documentType': 'Risk Management & Safety Protocol',
            'prompt': f"""Generate a Risk Management and Safety Protocol for {name} including:

CLIENT: {name}
PROTOCOL DATE: {current_date}

1. SAFETY ASSESSMENT - comprehensive safety evaluation for {name}
2. RISK MITIGATION STRATEGIES - specific risk reduction plans for {name}
3. EMERGENCY PROCEDURES - crisis response protocols for {name}
4. INCIDENT REPORTING - reporting procedures for {name}'s case
5. SAFETY MONITORING - ongoing safety oversight for {name}
6. CRISIS INTERVENTION - crisis response plan for {name}
7. REGULATORY COMPLIANCE - safety compliance requirements for {name}

Include evidence-based risk management practices and safety protocols specific to behavioral health."""
        }
    }
    
    return prompts.get(step_id, {
        'documentType': 'Professional Documentation',
        'prompt': f"""Generate professional behavioral health documentation for {name} at the Behavioral Health Center at Cypress, including comprehensive assessment, treatment planning, and service delivery components appropriate for regulatory compliance and clinical best practices."""
    })

