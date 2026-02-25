import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import json
from src.config import config

# Realistic contract templates
SAMPLE_CONTRACTS = [
    """SERVICE AGREEMENT

This Service Agreement (the "Agreement") is entered into as of January 15, 2024 (the "Effective Date") by and between ABC Corporation, a Delaware corporation with offices at 123 Business Ave, Wilmington, DE 19801 ("Company"), and XYZ Consulting Services Inc., a California corporation with offices at 456 Tech Street, San Francisco, CA 94102 ("Service Provider").

WHEREAS, Company desires to retain Service Provider to provide professional consulting services; and
WHEREAS, Service Provider agrees to provide such services under the terms set forth herein;

NOW, THEREFORE, in consideration of the mutual covenants and agreements herein contained, the parties agree as follows:

1. SERVICES AND DELIVERABLES
1.1 Service Provider agrees to provide business consulting and strategic planning services to Company as more particularly described in Exhibit A attached hereto and incorporated by reference (the "Services").
1.2 Service Provider shall deliver monthly progress reports and quarterly strategic assessments.

2. COMPENSATION AND PAYMENT TERMS
2.1 Company shall pay Service Provider a monthly retainer fee of Ten Thousand Dollars ($10,000.00).
2.2 Payment shall be made within thirty (30) days of receipt of invoice.
2.3 Late payments shall accrue interest at the rate of 1.5% per month.
2.4 Service Provider shall invoice Company on the first business day of each month.

3. TERM AND TERMINATION
3.1 This Agreement shall commence on the Effective Date and continue for an initial term of twelve (12) months.
3.2 Either party may terminate this Agreement upon sixty (60) days prior written notice to the other party.
3.3 Company may terminate this Agreement immediately for cause upon written notice if Service Provider materially breaches any provision herein.
3.4 Upon termination, Service Provider shall deliver all work product and materials to Company within ten (10) business days.

4. CONFIDENTIAL INFORMATION
4.1 Both parties acknowledge that they may have access to confidential and proprietary information of the other party.
4.2 Each party agrees to maintain the confidentiality of such information and not disclose it to any third party without prior written consent.
4.3 This confidentiality obligation shall survive termination of this Agreement for a period of five (5) years.
4.4 Confidential Information does not include information that: (a) is publicly available; (b) was known prior to disclosure; or (c) is independently developed.

5. INTELLECTUAL PROPERTY RIGHTS
5.1 All work product, deliverables, and materials created by Service Provider in connection with the Services shall be the exclusive property of Company.
5.2 Service Provider hereby assigns all right, title, and interest in such work product to Company.

6. REPRESENTATIONS AND WARRANTIES
6.1 Service Provider represents that it has the necessary expertise and resources to perform the Services.
6.2 Service Provider warrants that the Services will be performed in a professional and workmanlike manner.

7. LIMITATION OF LIABILITY
7.1 In no event shall either party's total liability under this Agreement exceed the total fees paid or payable hereunder in the twelve (12) months preceding the claim.
7.2 Neither party shall be liable for any indirect, incidental, consequential, or punitive damages.

8. GOVERNING LAW AND DISPUTE RESOLUTION
8.1 This Agreement shall be governed by and construed in accordance with the laws of the State of Delaware, without regard to conflicts of law principles.
8.2 Any disputes arising under this Agreement shall be resolved through binding arbitration in Wilmington, Delaware.

IN WITNESS WHEREOF, the parties have executed this Agreement as of the date first written above.""",

    """EMPLOYMENT AGREEMENT

This Employment Agreement (the "Agreement") is made and entered into as of March 1, 2024, by and between TechVenture Solutions Ltd., a Delaware corporation with its principal place of business at 789 Innovation Drive, Austin, TX 78701 (the "Employer"), and Jennifer Martinez (the "Employee").

RECITALS
WHEREAS, Employer desires to employ Employee as Senior Software Engineer; and
WHEREAS, Employee desires to accept such employment on the terms and conditions set forth herein;

NOW, THEREFORE, the parties agree as follows:

1. POSITION AND DUTIES
1.1 Employee shall serve in the position of Senior Software Engineer, reporting to the Chief Technology Officer.
1.2 Employee shall perform all duties and responsibilities customarily associated with such position, including but not limited to software development, code review, and technical documentation.
1.3 Employee shall devote Employee's full business time, attention, and energies to the performance of duties hereunder.

2. COMPENSATION AND BENEFITS
2.1 Base Salary: Employer shall pay Employee an annual base salary of One Hundred Twenty Thousand Dollars ($120,000.00), payable in bi-weekly installments.
2.2 Annual Bonus: Employee shall be eligible for an annual performance bonus of up to twenty percent (20%) of base salary, subject to achievement of performance objectives.
2.3 Stock Options: Employee shall be granted options to purchase 5,000 shares of Employer's common stock, vesting over four (4) years.
2.4 Health Benefits: Employee shall be entitled to participate in Employer's health insurance plan, including medical, dental, and vision coverage.
2.5 Retirement Plan: Employee may participate in Employer's 401(k) plan with company matching up to 4% of salary.
2.6 Paid Time Off: Employee shall accrue twenty (20) days of paid vacation per year, plus ten (10) paid holidays.

3. TERM OF EMPLOYMENT
3.1 This Agreement shall commence on April 1, 2024, and shall continue on an at-will basis until terminated by either party.
3.2 Either party may terminate this Agreement at any time, with or without cause, upon thirty (30) days prior written notice.

4. TERMINATION PROVISIONS
4.1 Termination for Cause: Employer may terminate Employee immediately for cause, including but not limited to: (a) material breach of this Agreement; (b) gross negligence or willful misconduct; (c) conviction of a felony; or (d) violation of company policies.
4.2 Severance: If Employer terminates Employee without cause, Employee shall receive severance pay equal to three (3) months of base salary.
4.3 Return of Property: Upon termination, Employee shall immediately return all company property, including laptop, access cards, and confidential materials.

5. NON-COMPETITION AND NON-SOLICITATION
5.1 During employment and for twelve (12) months following termination, Employee shall not:
    (a) Engage in any business competitive with Employer within a fifty (50) mile radius;
    (b) Solicit or attempt to solicit any customers or clients of Employer;
    (c) Solicit or hire any employees or contractors of Employer.
5.2 Employee acknowledges that this restriction is reasonable and necessary to protect Employer's legitimate business interests.

6. CONFIDENTIAL INFORMATION AND INTELLECTUAL PROPERTY
6.1 Employee acknowledges that during employment, Employee will have access to trade secrets and confidential information.
6.2 Employee agrees to maintain the confidentiality of such information both during and after employment.
6.3 All inventions, discoveries, and works of authorship created by Employee in connection with employment shall be the exclusive property of Employer.

7. GENERAL PROVISIONS
7.1 Governing Law: This Agreement shall be governed by the laws of the State of Texas.
7.2 Entire Agreement: This Agreement constitutes the entire agreement between the parties and supersedes all prior agreements.
7.3 Amendment: This Agreement may only be amended in writing signed by both parties.

IN WITNESS WHEREOF, the parties have executed this Agreement as of the date first written above.""",

    """COMMERCIAL LEASE AGREEMENT

This Commercial Lease Agreement (the "Lease") is entered into as of February 1, 2024, between Metropolitan Commercial Properties LLC, a New York limited liability company with offices at 555 Property Management Blvd, New York, NY 10001 (the "Landlord"), and Downtown Coffee House Inc., a New York corporation (the "Tenant").

1. PREMISES AND USE
1.1 Landlord hereby leases to Tenant the commercial space located at 123 Main Street, Ground Floor, New York, NY 10002 (the "Premises"), consisting of approximately 2,000 square feet.
1.2 The Premises shall be used solely for the operation of a coffee shop and café, and for no other purpose without Landlord's prior written consent.
1.3 Tenant shall have access to the Premises twenty-four (24) hours per day, seven (7) days per week.

2. LEASE TERM
2.1 The initial term of this Lease shall be five (5) years, commencing on March 1, 2024 (the "Commencement Date") and ending on February 28, 2029.
2.2 Tenant shall have the option to renew this Lease for two (2) additional five-year terms upon providing written notice at least six (6) months prior to expiration.

3. RENT AND ADDITIONAL CHARGES
3.1 Base Rent: Tenant shall pay monthly base rent of Five Thousand Dollars ($5,000.00) for the first year.
3.2 Rent Increases: Base rent shall increase by three percent (3%) annually on each anniversary of the Commencement Date.
3.3 Payment Terms: Rent is due on the first day of each month. Late payments shall incur a late fee of $250.00.
3.4 Common Area Maintenance (CAM): Tenant shall pay its proportionate share of CAM charges, estimated at $800 per month.
3.5 Property Taxes: Tenant shall reimburse Landlord for Tenant's proportionate share of real estate taxes.
3.6 Utilities: Tenant shall be responsible for all utilities, including electricity, gas, water, sewer, and internet.

4. SECURITY DEPOSIT
4.1 Tenant has deposited Ten Thousand Dollars ($10,000.00) as security for performance of Tenant's obligations.
4.2 The security deposit shall be returned within thirty (30) days after lease termination, less any deductions for damages or unpaid rent.
4.3 Landlord shall hold the deposit in an interest-bearing account and return accrued interest to Tenant.

5. MAINTENANCE AND REPAIRS
5.1 Landlord Responsibilities: Landlord shall maintain the structural components, roof, foundation, and common areas.
5.2 Tenant Responsibilities: Tenant shall maintain the interior of the Premises in good condition, including HVAC, plumbing, and electrical systems.
5.3 Repairs: Tenant shall promptly notify Landlord of any needed repairs to Landlord's responsibility areas.

6. IMPROVEMENTS AND ALTERATIONS
6.1 Tenant may make non-structural alterations with Landlord's prior written consent.
6.2 All improvements shall become the property of Landlord upon installation.
6.3 Tenant shall obtain all necessary permits and comply with building codes.

7. INSURANCE
7.1 Landlord shall maintain property insurance on the building.
7.2 Tenant shall maintain general liability insurance with minimum coverage of $2,000,000.
7.3 Tenant shall provide Landlord with certificates of insurance naming Landlord as additional insured.

8. DEFAULT AND REMEDIES
8.1 Events of Default include: (a) failure to pay rent within five (5) days of due date; (b) violation of lease terms; or (c) bankruptcy or insolvency.
8.2 Upon default, Landlord may: (a) terminate the Lease; (b) re-enter the Premises; (c) pursue all legal remedies; or (d) recover damages.
8.3 Tenant shall remain liable for all rent through the end of the term.

9. TERMINATION
9.1 Either party may terminate this Lease upon material breach by the other party, with sixty (60) days written notice and opportunity to cure.
9.2 Landlord may terminate immediately if Tenant uses Premises for illegal purposes.

10. GENERAL PROVISIONS
10.1 Assignment and Subletting: Tenant may not assign or sublet without Landlord's prior written consent.
10.2 Notices: All notices shall be in writing and sent to the addresses set forth above.
10.3 Governing Law: This Lease shall be governed by the laws of the State of New York.

IN WITNESS WHEREOF, the parties have executed this Lease as of the date first written above.""",

    """SOFTWARE LICENSE AND SUBSCRIPTION AGREEMENT

This Software License and Subscription Agreement (the "Agreement") is entered into as of January 10, 2024, between CloudTech Solutions Inc., a Delaware corporation with principal offices at 999 Software Park, Seattle, WA 98101 (the "Licensor"), and Enterprise Business Systems Corp., a Washington corporation (the "Licensee").

WHEREAS, Licensor has developed proprietary enterprise resource planning software; and
WHEREAS, Licensee desires to license and use such software;

NOW, THEREFORE, the parties agree as follows:

1. DEFINITIONS
1.1 "Software" means Licensor's CloudERP platform, version 5.0, including all updates and enhancements.
1.2 "Documentation" means user manuals, technical specifications, and training materials.
1.3 "Authorized Users" means Licensee's employees and contractors authorized to access the Software.
1.4 "Subscription Period" means the term during which Licensee has access rights to the Software.

2. LICENSE GRANT
2.1 Subject to the terms herein, Licensor grants Licensee a non-exclusive, non-transferable, limited license to use the Software.
2.2 The license permits up to 100 Authorized Users during the Subscription Period.
2.3 Licensee may use the Software solely for Licensee's internal business operations.
2.4 The Software shall be accessed via cloud-based deployment; Licensee shall not receive source code.

3. LICENSE RESTRICTIONS
3.1 Licensee shall not: (a) copy or modify the Software; (b) reverse engineer or decompile the Software; (c) sublicense or distribute the Software; (d) remove proprietary notices; or (e) use the Software for service bureau purposes.
3.2 Licensee shall implement reasonable security measures to prevent unauthorized access.

4. SUBSCRIPTION FEES AND PAYMENT
4.1 Annual Subscription Fee: Licensee shall pay an annual subscription fee of Sixty Thousand Dollars ($60,000.00).
4.2 Payment Terms: Fees are due within thirty (30) days of invoice date.
4.3 Implementation Fee: A one-time implementation fee of $15,000 is due upon execution of this Agreement.
4.4 Additional Users: Each additional user beyond 100 shall be charged at $50 per user per month.
4.5 Fee Increases: Licensor may increase fees upon renewal by up to five percent (5%) annually.

5. TERM AND RENEWAL
5.1 Initial Term: This Agreement shall commence on February 1, 2024, and continue for an initial term of three (3) years.
5.2 Renewal: This Agreement shall automatically renew for successive one-year terms unless either party provides ninety (90) days written notice of non-renewal.

6. SUPPORT AND MAINTENANCE
6.1 Technical Support: Licensor shall provide email and phone support during business hours (Monday-Friday, 8am-6pm PST).
6.2 Software Updates: Licensor shall provide all software updates, patches, and bug fixes at no additional charge.
6.3 Service Level Agreement: Licensor shall maintain 99.5% uptime, measured monthly. Downtime exceeding this shall result in pro-rata service credits.

7. WARRANTY AND DISCLAIMER
7.1 Licensor warrants that the Software will perform substantially in accordance with the Documentation for ninety (90) days.
7.2 Licensor's sole obligation for breach of warranty is to repair or replace the Software or refund fees paid.
7.3 EXCEPT AS EXPRESSLY PROVIDED, THE SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND.

8. LIMITATION OF LIABILITY
8.1 Licensor's total cumulative liability shall not exceed the fees paid by Licensee in the twelve (12) months preceding the claim.
8.2 Neither party shall be liable for indirect, incidental, consequential, or punitive damages, including lost profits.

9. CONFIDENTIALITY
9.1 Each party agrees to maintain the confidentiality of the other party's proprietary information.
9.2 This obligation shall survive termination for five (5) years.

10. TERMINATION
10.1 Either party may terminate this Agreement for material breach upon thirty (30) days written notice and failure to cure.
10.2 Licensor may suspend access immediately upon Licensee's failure to pay fees.
10.3 Upon termination, Licensee shall cease all use of the Software and return or destroy all copies.

11. DATA AND PRIVACY
11.1 Licensee retains all rights to data input into the Software.
11.2 Licensor shall comply with applicable data protection laws and maintain SOC 2 Type II certification.
11.3 Upon termination, Licensor shall return or delete Licensee's data within thirty (30) days.

12. GENERAL PROVISIONS
12.1 Governing Law: This Agreement shall be governed by Washington law.
12.2 Entire Agreement: This Agreement constitutes the entire understanding between the parties.
12.3 Assignment: Neither party may assign this Agreement without prior written consent.

IN WITNESS WHEREOF, the parties have executed this Agreement as of the date first written above.""",

    """MUTUAL NON-DISCLOSURE AGREEMENT

This Mutual Non-Disclosure Agreement (the "Agreement") is made and entered into as of April 5, 2024, by and between BioTech Innovations Inc., a Massachusetts corporation with offices at 321 Research Lane, Cambridge, MA 02138 (the "First Party"), and PharmaDev Research LLC, a Delaware limited liability company with offices at 654 Discovery Drive, San Diego, CA 92101 (the "Second Party"). First Party and Second Party are collectively referred to as the "Parties" and individually as a "Party."

WHEREAS, the Parties wish to explore a potential business relationship concerning collaborative research and development; and
WHEREAS, in connection therewith, each Party may disclose certain confidential and proprietary information to the other Party;

NOW, THEREFORE, in consideration of the mutual covenants contained herein, the Parties agree as follows:

1. PURPOSE
1.1 The Parties wish to explore a potential collaboration in the field of pharmaceutical development and clinical research (the "Purpose").
1.2 The exchange of information is solely for evaluating and discussing the potential business relationship.

2. DEFINITION OF CONFIDENTIAL INFORMATION
2.1 "Confidential Information" means all non-public information disclosed by one Party (the "Disclosing Party") to the other Party (the "Receiving Party"), whether orally, in writing, or in any other form, including but not limited to:
    (a) Technical data, research results, formulas, processes, designs, and know-how;
    (b) Business information, including marketing plans, financial data, customer lists, and supplier information;
    (c) Software, source code, algorithms, and technical specifications;
    (d) Any information marked or identified as "Confidential" or "Proprietary";
    (e) Any information that reasonably should be understood to be confidential given the nature of the information and circumstances of disclosure.

2.2 Confidential Information shall not include information that:
    (a) Is or becomes publicly available through no breach of this Agreement by the Receiving Party;
    (b) Was rightfully in the Receiving Party's possession prior to disclosure by the Disclosing Party;
    (c) Is rightfully received by the Receiving Party from a third party without breach of any confidentiality obligation;
    (d) Is independently developed by the Receiving Party without use of or reference to the Confidential Information; or
    (e) Is required to be disclosed by law or court order, provided that the Receiving Party provides prompt notice to the Disclosing Party.

3. OBLIGATIONS OF RECEIVING PARTY
3.1 The Receiving Party agrees to:
    (a) Hold all Confidential Information in strict confidence;
    (b) Not disclose Confidential Information to any third party without the prior written consent of the Disclosing Party;
    (c) Use the Confidential Information solely for the Purpose;
    (d) Limit access to Confidential Information to employees and consultants who have a legitimate need to know and who are bound by confidentiality obligations at least as restrictive as those contained herein;
    (e) Protect the Confidential Information using the same degree of care used to protect its own confidential information, but in no event less than reasonable care;
    (f) Not copy or reproduce Confidential Information except as necessary for the Purpose.

3.2 The Receiving Party shall be responsible for any breach of this Agreement by its employees, consultants, or agents.

4. TERM AND SURVIVAL
4.1 This Agreement shall commence on the date first written above and shall continue for a period of three (3) years, unless earlier terminated by either Party upon thirty (30) days written notice.
4.2 The confidentiality obligations set forth herein shall survive termination of this Agreement and shall continue for a period of five (5) years from the date of disclosure of each item of Confidential Information.

5. RETURN OR DESTRUCTION OF CONFIDENTIAL INFORMATION
5.1 Upon termination of this Agreement or upon request by the Disclosing Party, the Receiving Party shall, at the Disclosing Party's option:
    (a) Return all Confidential Information, including all copies, notes, and derivatives thereof; or
    (b) Destroy all Confidential Information and certify such destruction in writing.
5.2 Notwithstanding the foregoing, the Receiving Party may retain one archival copy of Confidential Information solely for legal compliance purposes.

6. NO LICENSE OR TRANSFER OF RIGHTS
6.1 This Agreement does not grant the Receiving Party any license, right, or interest in or to any Confidential Information, patents, copyrights, trademarks, or other intellectual property of the Disclosing Party.
6.2 All Confidential Information remains the sole property of the Disclosing Party.

7. NO OBLIGATION TO PROCEED
7.1 This Agreement does not obligate either Party to proceed with any transaction or relationship.
7.2 Neither Party shall have any obligation to disclose any particular Confidential Information.

8. REMEDIES AND INJUNCTIVE RELIEF
8.1 The Parties acknowledge that monetary damages may be inadequate to compensate for a breach of this Agreement.
8.2 The Disclosing Party shall be entitled to seek equitable relief, including injunction and specific performance, in addition to all other remedies available at law or in equity.
8.3 The prevailing party in any action to enforce this Agreement shall be entitled to recover reasonable attorneys' fees and costs.

9. REPRESENTATIONS AND WARRANTIES
9.1 Each Party represents and warrants that it has the authority to enter into this Agreement and to perform its obligations hereunder.
9.2 Each Party represents that the execution and performance of this Agreement will not violate any other agreement to which it is a party.

10. GENERAL PROVISIONS
10.1 Governing Law: This Agreement shall be governed by and construed in accordance with the laws of the State of Delaware, without regard to its conflicts of law principles.
10.2 Jurisdiction: The Parties consent to the exclusive jurisdiction of the state and federal courts located in Delaware.
10.3 Entire Agreement: This Agreement constitutes the entire agreement between the Parties and supersedes all prior agreements and understandings.
10.4 Amendment: This Agreement may only be amended by a writing signed by both Parties.
10.5 Severability: If any provision is found to be unenforceable, the remainder shall remain in full force and effect.
10.6 Waiver: No waiver of any provision shall be deemed a waiver of any other provision or subsequent breach.
10.7 Counterparts: This Agreement may be executed in counterparts, each of which shall constitute an original.

IN WITNESS WHEREOF, the Parties have caused this Agreement to be executed by their duly authorized representatives as of the date first written above."""
]

def create_contracts_and_qa():
    """Create sample contracts and QA pairs"""
    
    print("="*60)
    print("CREATING SAMPLE LEGAL CONTRACTS")
    print("="*60)
    
    # Create directories
    contracts_dir = config.RAW_DATA_DIR / "contracts"
    contracts_dir.mkdir(parents=True, exist_ok=True)
    config.PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    # Create contracts (10 copies of each template with variations)
    print("\n📄 Creating contract files...")
    file_count = 0
    
    for i in range(10):
        for idx, template in enumerate(SAMPLE_CONTRACTS):
            # Add variations
            year = 2020 + i
            contract = template.replace("2024", str(year))
            contract = contract.replace("$10,000", f"${10000 + (i * 1000)}")
            contract = contract.replace("$5,000", f"${5000 + (i * 500)}")
            contract = contract.replace("$120,000", f"${120000 + (i * 5000)}")
            
            file_path = contracts_dir / f"contract_{file_count:03d}.txt"
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(contract)
            
            print(f"  ✅ {file_path.name} ({len(contract):,} chars)")
            file_count += 1
    
    print(f"\n✅ Created {file_count} contract files")
    
    # Create QA pairs
    print("\n📝 Creating evaluation QA pairs...")
    
    qa_pairs = [
        {"question": "What are the payment terms in the service agreement?", "context": "Service agreement payment terms"},
        {"question": "What is the termination notice period?", "context": "Termination clause"},
        {"question": "What are the confidentiality obligations?", "context": "Confidentiality terms"},
        {"question": "Who are the parties to the contract?", "context": "Contract parties"},
        {"question": "What is the term of the agreement?", "context": "Agreement duration"},
        {"question": "What are the employee benefits?", "context": "Employment benefits"},
        {"question": "What is the monthly rent amount?", "context": "Lease rent"},
        {"question": "What are the late payment fees?", "context": "Late fees"},
        {"question": "What is the security deposit amount?", "context": "Security deposit"},
        {"question": "What are the maintenance responsibilities?", "context": "Maintenance terms"},
        {"question": "What are the intellectual property rights?", "context": "IP rights"},
        {"question": "What is the limitation of liability?", "context": "Liability limits"},
        {"question": "What is the governing law?", "context": "Legal jurisdiction"},
        {"question": "What are the non-compete restrictions?", "context": "Non-compete clause"},
        {"question": "What is the subscription fee?", "context": "License fees"},
        {"question": "What are the warranty terms?", "context": "Warranty provisions"},
        {"question": "What are the support services included?", "context": "Support terms"},
        {"question": "What triggers a default?", "context": "Default conditions"},
        {"question": "How can the agreement be terminated early?", "context": "Early termination"},
        {"question": "What happens to confidential information after termination?", "context": "Post-termination obligations"}
    ]
    
    # Expand to 100 QA pairs
    expanded_qa = []
    for i in range(5):
        for qa in qa_pairs:
            expanded_qa.append({
                'question': qa['question'],
                'context': qa['context'],
                'document_id': f"contract_{(i * 10):03d}.txt"
            })
    
    # Save QA pairs
    eval_path = config.PROCESSED_DATA_DIR / "eval_qa.jsonl"
    with open(eval_path, 'w', encoding='utf-8') as f:
        for qa in expanded_qa[:100]:
            f.write(json.dumps(qa) + '\n')
    
    print(f"✅ Created {len(expanded_qa[:100])} QA pairs")
    print(f"   Saved to: {eval_path}")
    
    # Verification
    print("\n" + "="*60)
    print("VERIFICATION")
    print("="*60)
    
    saved_files = list(contracts_dir.glob("*.txt"))
    print(f"📁 Contract files: {len(saved_files)}")
    print(f"📁 Location: {contracts_dir}")
    print(f"📝 QA pairs: 100")
    print(f"📝 Location: {eval_path}")
    
    # Show sample
    if saved_files:
        sample_file = saved_files[0]
        with open(sample_file, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"\n📋 Sample file: {sample_file.name}")
        print(f"   Length: {len(content):,} characters")
        print(f"   Preview: {content[:200]}...")
    
    print("\n" + "="*60)
    print("✅ SAMPLE DATA CREATION COMPLETE!")
    print("="*60)
    print("\nNext step: python scripts/manual_index_build.py")

if __name__ == "__main__":
    create_contracts_and_qa()