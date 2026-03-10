from tools.database import Lead, get_db
from datetime import datetime
import re

def extract_lead_details(lead_info: str, qualification_report: str) -> dict:
    """
    Extract structured data from lead info and qualification report
    """
    # Extract email
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, lead_info)
    email = emails[0] if emails else None
    
    # Extract phone (basic pattern)
    phone_pattern = r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]'
    phones = re.findall(phone_pattern, lead_info)
    phone = phones[0] if phones else None
    
    # Extract company name (first capitalized words before comma)
    company_match = re.search(r'^([A-Z][A-Za-z\s&]+?)(?:,|\s+company|\s+\d)', lead_info)
    company_name = company_match.group(1).strip() if company_match else "Unknown Company"
    
    # Extract BANT scores from report
    budget_score = extract_score(qualification_report, "budget")
    authority_score = extract_score(qualification_report, "authority")
    need_score = extract_score(qualification_report, "need")
    timeline_score = extract_score(qualification_report, "timeline")
    overall_score = extract_score(qualification_report, "overall|total|score")
    
    # Extract conversion probability
    prob_match = re.search(r'(\d+)%?\s*(?:probability|chance|likelihood)', qualification_report.lower())
    conversion_probability = float(prob_match.group(1)) / 100 if prob_match else 0.5
    
    # Extract recommended actions
    actions_match = re.search(r'(?:recommended actions?|next steps?):(.+?)(?:\n\n|\Z)', qualification_report, re.IGNORECASE | re.DOTALL)
    recommended_actions = actions_match.group(1).strip() if actions_match else "Contact lead for discovery call"
    
    return {
        'company_name': company_name,
        'email': email,
        'phone': phone,
        'budget_score': budget_score,
        'authority_score': authority_score,
        'need_score': need_score,
        'timeline_score': timeline_score,
        'overall_score': overall_score,
        'conversion_probability': conversion_probability,
        'recommended_actions': recommended_actions
    }

def extract_score(text: str, keyword: str) -> int:
    """Extract numerical score for a keyword from text"""
    pattern = rf'{keyword}[:\s]*(\d+)(?:/100)?'
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        score = int(match.group(1))
        return min(score, 100)  # Cap at 100
    return 50  # Default middle score

def save_lead_to_crm(lead_info: str, qualification_report: str, market: str = None, industry: str = None) -> dict:
    """
    Save qualified lead to CRM database
    """
    try:
        db = get_db()
        
        # Extract details
        details = extract_lead_details(lead_info, qualification_report)
        
        # Create lead record
        lead = Lead(
            company_name=details['company_name'],
            email=details['email'],
            phone=details['phone'],
            market=market or "Unknown",
            industry=industry or "Unknown",
            budget_score=details['budget_score'],
            authority_score=details['authority_score'],
            need_score=details['need_score'],
            timeline_score=details['timeline_score'],
            overall_score=details['overall_score'],
            lead_info=lead_info,
            qualification_report=qualification_report,
            recommended_actions=details['recommended_actions'],
            conversion_probability=details['conversion_probability'],
            status='qualified'
        )
        
        db.add(lead)
        db.commit()
        db.refresh(lead)
        
        return {
            "success": True,
            "message": f"Lead saved to CRM with ID: {lead.id}",
            "lead_id": lead.id,
            "company": details['company_name'],
            "score": details['overall_score']
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Error saving to CRM: {str(e)}"
        }

def get_all_leads(status: str = None, min_score: int = 0):
    """
    Retrieve leads from CRM
    """
    try:
        db = get_db()
        query = db.query(Lead)
        
        if status:
            query = query.filter(Lead.status == status)
        
        if min_score > 0:
            query = query.filter(Lead.overall_score >= min_score)
        
        leads = query.order_by(Lead.overall_score.desc()).all()
        
        return {
            "success": True,
            "count": len(leads),
            "leads": [
                {
                    "id": lead.id,
                    "company": lead.company_name,
                    "email": lead.email,
                    "score": lead.overall_score,
                    "probability": f"{lead.conversion_probability * 100:.0f}%",
                    "status": lead.status,
                    "created": lead.created_at.strftime("%Y-%m-%d %H:%M")
                }
                for lead in leads
            ]
        }
    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        }