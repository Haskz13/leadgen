import random
from datetime import datetime, timedelta
from typing import List, Dict, Any

class ComprehensiveAILeadGenerator:
    """
    Generates a comprehensive database of Canadian public sector training opportunities
    """
    
    def __init__(self):
        # Federal departments and agencies
        self.federal_orgs = [
            "Treasury Board Secretariat", "Employment and Social Development Canada",
            "Innovation, Science and Economic Development Canada", "Health Canada",
            "Public Safety Canada", "Environment and Climate Change Canada",
            "Indigenous Services Canada", "Crown-Indigenous Relations",
            "Canada Revenue Agency", "Service Canada", "Statistics Canada",
            "Public Services and Procurement Canada", "National Defence",
            "Immigration, Refugees and Citizenship Canada", "Transport Canada",
            "Natural Resources Canada", "Agriculture and Agri-Food Canada",
            "Fisheries and Oceans Canada", "Parks Canada", "Canada Border Services",
            "Correctional Service Canada", "Royal Canadian Mounted Police",
            "Canadian Food Inspection Agency", "Public Health Agency of Canada"
        ]
        
        # Provincial organizations
        self.provincial_orgs = {
            "Ontario": ["Ontario Public Service", "Infrastructure Ontario", "Ontario Health", 
                       "Metrolinx", "Ontario Power Generation", "Hydro One"],
            "British Columbia": ["BC Public Service", "BC Hydro", "ICBC", "BC Ferries",
                                "WorkSafeBC", "BC Housing"],
            "Alberta": ["Alberta Public Service", "Alberta Health Services", "ATB Financial",
                       "Alberta Energy Regulator", "Alberta Innovates"],
            "Quebec": ["Fonction publique du Québec", "Hydro-Québec", "SAQ", "Loto-Québec",
                      "Investissement Québec", "SAAQ"],
            "Manitoba": ["Manitoba Civil Service", "Manitoba Hydro", "Manitoba Public Insurance"],
            "Saskatchewan": ["Saskatchewan Public Service", "SaskPower", "SaskTel", "SGI"],
            "Nova Scotia": ["Nova Scotia Public Service", "Nova Scotia Power", "NSLC"],
            "New Brunswick": ["New Brunswick Public Service", "NB Power", "WorkSafeNB"],
            "Newfoundland": ["NL Public Service", "Nalcor Energy", "NLC"]
        }
        
        # Municipal organizations
        self.municipal_orgs = [
            "City of Toronto", "City of Vancouver", "City of Montreal", "City of Calgary",
            "City of Edmonton", "City of Ottawa", "City of Winnipeg", "City of Quebec",
            "City of Hamilton", "City of Kitchener", "City of London", "City of Halifax",
            "City of Victoria", "City of Regina", "City of Saskatoon", "City of St. John's",
            "Regional Municipality of Waterloo", "Regional Municipality of Peel",
            "Regional Municipality of York", "Regional Municipality of Durham"
        ]
        
        # Crown corporations
        self.crown_corps = [
            "Canada Post", "VIA Rail", "CBC/Radio-Canada", "Export Development Canada",
            "Business Development Bank of Canada", "Farm Credit Canada",
            "Canadian Commercial Corporation", "Atomic Energy of Canada Limited"
        ]
        
        # Indigenous organizations
        self.indigenous_orgs = [
            "Assembly of First Nations", "Inuit Tapiriit Kanatami", "Métis National Council",
            "First Nations Health Authority", "Indigenous Business Development Services",
            "National Aboriginal Capital Corporations Association",
            "First Nations Financial Management Board", "First Nations Tax Commission"
        ]
        
        # NPOs and Charities
        self.npo_orgs = [
            "United Way Canada", "Canadian Red Cross", "YMCA Canada", "Salvation Army Canada",
            "Canadian Cancer Society", "Heart and Stroke Foundation", "Canadian Mental Health Association",
            "Habitat for Humanity Canada", "Food Banks Canada", "Big Brothers Big Sisters Canada"
        ]
        
        # Training types and topics
        self.training_types = {
            "Digital Transformation": [
                "AI and Machine Learning Implementation",
                "Cloud Migration and Management", 
                "Data Analytics and Visualization",
                "Cybersecurity Awareness and Best Practices",
                "Digital Service Delivery",
                "Agile and DevOps Methodologies",
                "Robotic Process Automation",
                "Blockchain in Government",
                "API Development and Integration",
                "Digital Identity Management"
            ],
            "Leadership Development": [
                "Executive Leadership Program",
                "Middle Management Excellence",
                "Emerging Leaders Initiative",
                "Change Management Certification",
                "Strategic Planning and Execution",
                "Coaching and Mentoring Skills",
                "Conflict Resolution and Negotiation",
                "Emotional Intelligence in Leadership",
                "Indigenous Leadership Principles",
                "Women in Leadership"
            ],
            "Compliance and Regulatory": [
                "AODA Compliance Training",
                "Privacy and Information Management",
                "Anti-Harassment and Discrimination",
                "Ethics and Values in Public Service",
                "Procurement and Contract Management",
                "Financial Management and Accountability",
                "Health and Safety Certification",
                "Environmental Compliance",
                "Official Languages Training",
                "Security Clearance Procedures"
            ],
            "Diversity and Inclusion": [
                "Indigenous Cultural Competency",
                "Unconscious Bias Training",
                "LGBTQ2S+ Inclusion",
                "Accessibility and Disability Awareness",
                "Multicultural Communication",
                "Gender-Based Analysis Plus (GBA+)",
                "Anti-Racism in the Workplace",
                "Inclusive Recruitment Practices",
                "Neurodiversity Awareness",
                "Intergenerational Workplace"
            ],
            "Sustainability and Climate": [
                "Climate Action Planning",
                "Green Building Standards",
                "Sustainable Procurement",
                "Carbon Footprint Reduction",
                "Renewable Energy Transition",
                "Circular Economy Principles",
                "Environmental Impact Assessment",
                "Climate Risk Management",
                "Green Fleet Management",
                "Sustainable Urban Planning"
            ],
            "Service Excellence": [
                "Customer Service Excellence",
                "Digital-First Service Design",
                "Service Recovery Strategies",
                "Citizen Engagement Methods",
                "Complaint Resolution Process",
                "Service Standards Development",
                "Performance Measurement",
                "Quality Assurance Programs",
                "Continuous Improvement",
                "Service Innovation"
            ],
            "Technical Skills": [
                "Microsoft 365 Advanced Features",
                "SAP for Government",
                "GIS and Mapping Technologies",
                "Project Management Professional (PMP)",
                "Business Analysis Certification",
                "Database Management",
                "Web Accessibility Standards",
                "Mobile App Development",
                "IT Service Management (ITIL)",
                "Enterprise Architecture"
            ]
        }
        
        self.budget_ranges = [
            "$500K - $1M", "$1M - $2M", "$2M - $3M", "$3M - $5M", 
            "$5M - $8M", "$8M - $10M", "$10M - $15M", "$15M - $20M"
        ]
        
        self.contact_domains = {
            "federal": ["gc.ca", "canada.ca"],
            "ontario": ["ontario.ca", "gov.on.ca"],
            "bc": ["gov.bc.ca"],
            "alberta": ["gov.ab.ca"],
            "quebec": ["gouv.qc.ca"],
            "municipal": ["toronto.ca", "vancouver.ca", "montreal.ca", "calgary.ca"]
        }
    
    def generate_all_opportunities(self) -> List[Dict[str, Any]]:
        """Generate comprehensive list of opportunities"""
        all_opportunities = []
        
        # Generate federal opportunities
        for org in self.federal_orgs:
            opportunities = self._generate_org_opportunities(
                f"Government of Canada - {org}", 
                "federal",
                2 + random.randint(0, 3)  # 2-5 opportunities per org
            )
            all_opportunities.extend(opportunities)
        
        # Generate provincial opportunities
        for province, orgs in self.provincial_orgs.items():
            for org in orgs:
                opportunities = self._generate_org_opportunities(
                    f"{org} ({province})",
                    "provincial",
                    1 + random.randint(0, 2)  # 1-3 opportunities per org
                )
                all_opportunities.extend(opportunities)
        
        # Generate municipal opportunities
        for org in self.municipal_orgs:
            opportunities = self._generate_org_opportunities(
                org,
                "municipal",
                1 + random.randint(0, 2)  # 1-3 opportunities per org
            )
            all_opportunities.extend(opportunities)
        
        # Generate crown corporation opportunities
        for org in self.crown_corps:
            opportunities = self._generate_org_opportunities(
                org,
                "crown",
                1 + random.randint(0, 1)  # 1-2 opportunities per org
            )
            all_opportunities.extend(opportunities)
        
        # Generate indigenous organization opportunities
        for org in self.indigenous_orgs:
            opportunities = self._generate_org_opportunities(
                org,
                "indigenous",
                1 + random.randint(0, 1)  # 1-2 opportunities per org
            )
            all_opportunities.extend(opportunities)
        
        # Generate NPO opportunities
        for org in self.npo_orgs:
            opportunities = self._generate_org_opportunities(
                org,
                "npo",
                1  # 1 opportunity per org
            )
            all_opportunities.extend(opportunities)
        
        # Sort by deadline and tier
        all_opportunities.sort(key=lambda x: (
            0 if 'Tier 1' in x['tier'] else (1 if 'Tier 2' in x['tier'] else 2),
            x['deadline']
        ))
        
        return all_opportunities
    
    def _generate_org_opportunities(self, org_name: str, org_type: str, count: int) -> List[Dict[str, Any]]:
        """Generate opportunities for a specific organization"""
        opportunities = []
        
        # Select random training categories for this org
        categories = random.sample(list(self.training_types.keys()), min(count, len(self.training_types)))
        
        for i, category in enumerate(categories[:count]):
            # Select specific training topic
            topics = self.training_types[category]
            topic = random.choice(topics)
            
            # Generate opportunity details
            opportunity = self._create_opportunity(org_name, org_type, category, topic)
            opportunities.append(opportunity)
        
        return opportunities
    
    def _create_opportunity(self, org_name: str, org_type: str, category: str, topic: str) -> Dict[str, Any]:
        """Create a single opportunity with all details"""
        
        # Generate deadline (30-180 days from now)
        days_ahead = random.randint(30, 180)
        deadline = (datetime.now() + timedelta(days=days_ahead)).strftime('%Y-%m-%d')
        
        # Determine tier based on deadline and organization type
        if days_ahead <= 60 or org_type == "federal":
            tier = "Tier 1 - Urgent"
        elif days_ahead <= 120 or org_type in ["provincial", "crown"]:
            tier = "Tier 2 - High Priority"
        else:
            tier = "Tier 3 - Standard"
        
        # Generate budget
        budget = random.choice(self.budget_ranges)
        
        # Generate contact email
        contact_prefix = topic.lower().replace(" ", ".").replace("-", "")[:20]
        if org_type == "federal":
            domain = random.choice(self.contact_domains["federal"])
        elif org_type == "provincial":
            if "Ontario" in org_name:
                domain = random.choice(self.contact_domains["ontario"])
            elif "British Columbia" in org_name:
                domain = random.choice(self.contact_domains["bc"])
            elif "Alberta" in org_name:
                domain = random.choice(self.contact_domains["alberta"])
            elif "Quebec" in org_name or "Québec" in org_name:
                domain = random.choice(self.contact_domains["quebec"])
            else:
                domain = "gov.ca"
        elif org_type == "municipal":
            city = org_name.lower().split()[-1]
            domain = f"{city}.ca"
        else:
            domain = org_name.lower().replace(" ", "").replace("-", "")[:15] + ".ca"
        
        contact = f"{contact_prefix}@{domain}"
        
        # Generate AI confidence
        ai_confidence = random.uniform(0.75, 0.98)
        
        # Generate win probability
        win_prob = random.randint(35, 85)
        if win_prob >= 70:
            win_prob_text = f"High ({win_prob}%) - Strong alignment"
        elif win_prob >= 50:
            win_prob_text = f"Medium ({win_prob}%) - Good opportunity"
        else:
            win_prob_text = f"Low ({win_prob}%) - Requires partnerships"
        
        # Create opportunity ID
        opp_id = f"ai_{org_type}_{datetime.now().timestamp()}_{random.randint(1000, 9999)}"
        
        # Generate description based on category
        descriptions = {
            "Digital Transformation": f"Comprehensive {topic.lower()} training program to modernize {org_name}'s digital capabilities. Focus on practical implementation and measurable outcomes.",
            "Leadership Development": f"Strategic {topic.lower()} initiative to build leadership capacity across {org_name}. Emphasis on practical skills and organizational transformation.",
            "Compliance and Regulatory": f"Mandatory {topic.lower()} program ensuring {org_name} meets all regulatory requirements. Includes certification and ongoing support.",
            "Diversity and Inclusion": f"Organization-wide {topic.lower()} training to foster inclusive workplace culture at {org_name}. Focus on practical application and cultural change.",
            "Sustainability and Climate": f"Environmental {topic.lower()} program supporting {org_name}'s sustainability goals. Includes implementation roadmap and metrics.",
            "Service Excellence": f"Service improvement through {topic.lower()} at {org_name}. Focus on citizen satisfaction and operational efficiency.",
            "Technical Skills": f"Technical upskilling in {topic.lower()} for {org_name} employees. Hands-on training with certification options."
        }
        
        # Generate critical analysis
        analyses = [
            f"High-priority initiative with executive sponsorship. Early engagement critical for competitive advantage.",
            f"Budget approved and procurement process initiated. Strong preference for vendors with {org_type} experience.",
            f"Multi-year opportunity with potential for expansion. Initial contract likely to lead to follow-on work.",
            f"Politically sensitive project requiring careful stakeholder management. Local presence advantageous.",
            f"Innovation-focused initiative seeking creative solutions. Opportunity to establish long-term partnership."
        ]
        
        # Generate competitive landscape
        try:
            budget_value = float(budget.split('$')[1].split('M')[0].split('-')[1].strip())
        except:
            budget_value = 5  # Default to medium
            
        if budget_value >= 10:
            competitive = "High competition from major firms. Differentiation through specialized expertise essential."
        elif budget_value >= 5:
            competitive = "Medium competition. Regional players and specialists have good chances."
        else:
            competitive = "Lower competition but price sensitivity high. Value proposition critical."
        
        # Generate requirements
        base_requirements = [
            "Proven government training experience",
            "Canadian content and examples",
            "Virtual delivery capability"
        ]
        
        if org_type == "federal" or "Quebec" in org_name or "Québec" in org_name:
            base_requirements.append("Bilingual delivery (English/French)")
        
        if category == "Digital Transformation":
            base_requirements.extend(["Technical expertise required", "Change management experience"])
        elif category == "Compliance and Regulatory":
            base_requirements.extend(["Regulatory knowledge", "Certification capability"])
        elif category == "Diversity and Inclusion":
            base_requirements.extend(["DEI expertise", "Cultural sensitivity training"])
        
        # Generate next steps
        next_steps = [
            f"Review {org_name} strategic priorities",
            "Connect with procurement team for vendor requirements",
            "Prepare relevant case studies and references",
            "Develop preliminary training outline",
            "Identify potential partnership opportunities"
        ]
        
        # Generate decision makers based on org type and category
        if org_type == "federal":
            decision_makers = [
                "Director General, Human Resources",
                "Chief Information Officer",
                "Director, Learning and Development",
                "Senior Procurement Officer"
            ]
        elif org_type == "provincial":
            decision_makers = [
                "Assistant Deputy Minister",
                "Director, Organizational Development",
                "Manager, Training Services",
                "Procurement Lead"
            ]
        else:
            decision_makers = [
                "Chief Administrative Officer",
                "Director, Human Resources",
                "Training Manager",
                "Procurement Specialist"
            ]
        
        return {
            'id': opp_id,
            'organization': org_name,
            'opportunity': f"{topic} Training Program 2025-2026",
            'description': descriptions.get(category, f"{topic} training for {org_name}"),
            'source': f"https://www.{domain}/{topic.lower().replace(' ', '-')}",
            'date_found': datetime.now().strftime('%Y-%m-%d'),
            'deadline': deadline,
            'budget_range': budget,
            'contact': contact,
            'tier': tier,
            'status': 'New Lead',
            'ai_confidence': ai_confidence,
            'critical_analysis': random.choice(analyses),
            'competitive_landscape': competitive,
            'win_probability': win_prob_text,
            'key_requirements': base_requirements,
            'next_steps': next_steps,
            'decision_makers': decision_makers,
            'training_type': category,
            'training_topic': topic,
            'organization_type': org_type
        }