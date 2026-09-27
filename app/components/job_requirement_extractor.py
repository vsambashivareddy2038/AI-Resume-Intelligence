import re
from app.components.skill_extractor import SkillExtractor

class JobRequirementExtractor:
    SECTION_ALIASES = {'responsibilities': ['responsibilities', 'key responsibilities', 'roles and responsibilities', 'duties', 'job responsibilities'], 'required_skills': ['required skills', 'required skill', 'required qualifications', 'requirements', 'technical skills', 'must have skills', 'must-have skills'], 'preferred_skills': ['preferred skills', 'preferred skill', 'preferred qualifications', 'nice to have', 'nice-to-have', 'good to have', 'good-to-have', 'optional skills'], 'education': ['education', 'educational qualifications', 'educational requirements', 'academic qualifications', 'academic requirements'], 'experience': ['experience', 'experience requirements', 'experience required', 'professional experience', 'work experience']}

    def __init__(self, skill_file='data/skills.csv'):
        self.skill_extractor = SkillExtractor(skill_file)

    # Normalize JD text before parsing.
    def _normalize_text(self, text):
        if not text:
            return ''
        text = text.replace('\r\n', '\n')
        text = text.replace('\r', '\n')
        text = text.replace('\t', ' ')
        text = re.sub('[ ]+', ' ', text)
        text = re.sub('\\n+', '\n', text)
        return text.strip()

    def _clean_section_text(self, text):
        if not text:
            return ''
        text = self._normalize_text(text)
        text = re.sub('(?m)^[\\s]*[-•●▪◦]\\s*', '', text)
        return text.strip()

    def _get_lines(self, text):
        if not text:
            return []
        text = text.replace('\r\n', '\n')
        text = text.replace('\r', '\n')
        return [line.strip() for line in text.splitlines() if line.strip()]

    def _section_heading_pattern(self, aliases):
        escaped = [re.escape(alias) for alias in aliases]
        return '(?<![a-zA-Z])(?:' + '|'.join(escaped) + ')\\s*:?(?![a-zA-Z])'

    # Find section headings without matching normal sentences.
    def _find_heading_positions(self, text):
        normalized = self._normalize_text(text)
        positions = []
        for section_name, aliases in self.SECTION_ALIASES.items():
            pattern = self._section_heading_pattern(aliases)
            for match in re.finditer(pattern, normalized, re.IGNORECASE):
                start = match.start()
                end = match.end()
                before = normalized[:start]
                after = normalized[end:]
                previous_char = before[-1] if before else ''
                next_char = after[0] if after else ''
                matched_text = match.group(0)
                has_colon = ':' in matched_text
                starts_line = start == 0 or previous_char == '\n'
                followed_by_newline = next_char == '\n'
                if not (starts_line or has_colon or followed_by_newline):
                    continue
                if section_name == 'experience' and (not starts_line) and (not has_colon) and (not followed_by_newline):
                    continue
                positions.append({'section': section_name, 'start': start, 'end': end, 'heading': matched_text})
        positions.sort(key=lambda item: item['start'])
        cleaned = []
        for item in positions:
            if not cleaned:
                cleaned.append(item)
                continue
            previous = cleaned[-1]
            if item['start'] < previous['end']:
                current_length = item['end'] - item['start']
                previous_length = previous['end'] - previous['start']
                if current_length > previous_length:
                    cleaned[-1] = item
            else:
                cleaned.append(item)
        return (normalized, cleaned)

    def _extract_section(self, text, section_name):
        if not text:
            return ''
        normalized, headings = self._find_heading_positions(text)
        target = None
        for heading in headings:
            if heading['section'] == section_name:
                target = heading
                break
        if target is None:
            return ''
        start = target['end']
        end = len(normalized)
        for heading in headings:
            if heading['start'] <= start:
                continue
            end = heading['start']
            break
        section_text = normalized[start:end]
        return self._clean_section_text(section_text)

    # Extract the job title from the JD.
    def extract_role(self, job_description):
        if not job_description:
            return None
        normalized = self._normalize_text(job_description)
        if not normalized:
            return None
        explicit_patterns = ['\\bjob\\s+title\\s*:\\s*(.+?)(?=\\babout\\s+the\\s+role\\b|\\bresponsibilities\\b|\\brequired\\s+skills\\b|\\bpreferred\\s+skills\\b|\\beducation\\b|\\bexperience\\b|$)', '\\bposition\\s+title\\s*:\\s*(.+?)(?=\\babout\\s+the\\s+role\\b|\\bresponsibilities\\b|\\brequired\\s+skills\\b|\\bpreferred\\s+skills\\b|\\beducation\\b|\\bexperience\\b|$)', '\\bposition\\s*:\\s*(.+?)(?=\\babout\\s+the\\s+role\\b|\\bresponsibilities\\b|\\brequired\\s+skills\\b|\\bpreferred\\s+skills\\b|\\beducation\\b|\\bexperience\\b|$)', '\\brole\\s*:\\s*(.+?)(?=\\babout\\s+the\\s+role\\b|\\bresponsibilities\\b|\\brequired\\s+skills\\b|\\bpreferred\\s+skills\\b|\\beducation\\b|\\bexperience\\b|$)']
        for pattern in explicit_patterns:
            match = re.search(pattern, normalized, re.IGNORECASE)
            if match:
                role = match.group(1).strip()
                role = re.sub('\\s+', ' ', role)
                if role:
                    return role
        lines = self._get_lines(job_description)
        if lines:
            first_line = lines[0].strip()
            first_line = re.sub('^job\\s+title\\s*:\\s*', '', first_line, flags=re.IGNORECASE)
            if first_line and len(first_line.split()) <= 10 and self._looks_like_role(first_line):
                return first_line
        role_keywords = ['engineer', 'developer', 'scientist', 'analyst', 'architect', 'manager', 'consultant', 'specialist', 'intern', 'administrator', 'researcher', 'designer']
        for line in lines[:10]:
            lower_line = line.lower()
            if len(line.split()) > 10:
                continue
            if any((keyword in lower_line for keyword in role_keywords)):
                return line.strip()
        return None

    def _looks_like_role(self, text):
        role_keywords = ['engineer', 'developer', 'scientist', 'analyst', 'architect', 'manager', 'consultant', 'specialist', 'intern', 'administrator', 'researcher', 'designer']
        lower = text.lower()
        return any((keyword in lower for keyword in role_keywords))

    # Get skills the job explicitly requires.
    def extract_required_skills(self, job_description):
        if not job_description:
            return []
        section = self._extract_section(job_description, 'required_skills')
        if section:
            skills = self.skill_extractor.extract_skills(section)
            return sorted(set(skills))
        normalized = self._normalize_text(job_description)
        preferred_section = self._extract_section(job_description, 'preferred_skills')
        text = normalized
        if preferred_section:
            text = text.replace(preferred_section, '')
        skills = self.skill_extractor.extract_skills(text)
        return sorted(set(skills))

    # Get optional or preferred skills.
    def extract_preferred_skills(self, job_description):
        if not job_description:
            return []
        section = self._extract_section(job_description, 'preferred_skills')
        if not section:
            return []
        skills = self.skill_extractor.extract_skills(section)
        return sorted(set(skills))

    # Extract the education level and field.
    def extract_education_requirement(self, job_description):
        result = {'degree_level': None, 'fields': [], 'raw_text': None}
        if not job_description:
            return result
        education_text = self._extract_section(job_description, 'education')
        if not education_text:
            normalized = self._normalize_text(job_description)
            education_matches = re.findall('[^.]*(?:bachelor|master|b\\.?\\s*tech|b\\.?\\s*e\\.?|b\\.?\\s*sc|m\\.?\\s*tech|m\\.?\\s*e\\.?|m\\.?\\s*sc|bca|mca|mba|ph\\.?\\s*d\\.?)[^.]*', normalized, re.IGNORECASE)
            if education_matches:
                education_text = ' '.join(education_matches).strip()
        if not education_text:
            return result
        education_text = self._clean_section_text(education_text)
        result['raw_text'] = education_text
        degree_patterns = [("\\bbachelor(?:'s)?\\b", 'bachelor'), ('\\bb\\.?\\s*tech\\b', 'bachelor'), ('\\bb\\.?\\s*e\\.?\\b', 'bachelor'), ('\\bb\\.?\\s*sc\\.?\\b', 'bachelor'), ('\\bbca\\b', 'bachelor'), ("\\bmaster(?:'s)?\\b", 'master'), ('\\bm\\.?\\s*tech\\b', 'master'), ('\\bm\\.?\\s*e\\.?\\b', 'master'), ('\\bm\\.?\\s*sc\\.?\\b', 'master'), ('\\bmca\\b', 'master'), ('\\bmba\\b', 'master'), ('\\bph\\.?\\s*d\\.?\\b', 'phd')]
        for pattern, level in degree_patterns:
            if re.search(pattern, education_text, re.IGNORECASE):
                result['degree_level'] = level
                break
        fields = ['computer science', 'artificial intelligence', 'data science', 'information technology', 'information systems', 'machine learning', 'software engineering', 'computer engineering', 'electronics', 'electrical engineering', 'cyber security', 'cybersecurity', 'mathematics', 'statistics']
        for field in fields:
            if re.search('\\b' + re.escape(field) + '\\b', education_text, re.IGNORECASE):
                result['fields'].append(field)
        result['fields'] = sorted(set(result['fields']))
        return result

    # Extract the required years of experience.
    def extract_experience_requirement(self, job_description):
        result = {'min_years': 0.0, 'max_years': None, 'experience_required': False, 'raw_text': None}
        if not job_description:
            return result
        experience_text = self._extract_section(job_description, 'experience')
        if not experience_text:
            normalized = self._normalize_text(job_description)
            matches = re.findall('[^.\\n]*\\b\\d+(?:\\.\\d+)?\\s*(?:-|–|—|to|\\+)?\\s*\\d*\\s*years?\\b[^.\\n]*', normalized, re.IGNORECASE)
            if matches:
                experience_text = ' '.join(matches).strip()
        if not experience_text:
            return result
        experience_text = self._clean_section_text(experience_text)
        if not re.search('\\byears?\\b', experience_text, re.IGNORECASE):
            return result
        result['raw_text'] = experience_text
        result['experience_required'] = True
        range_match = re.search('(\\d+(?:\\.\\d+)?)\\s*(?:-|–|—|to)\\s*(\\d+(?:\\.\\d+)?)\\s*years?', experience_text, re.IGNORECASE)
        if range_match:
            result['min_years'] = float(range_match.group(1))
            result['max_years'] = float(range_match.group(2))
            return result
        plus_match = re.search('(\\d+(?:\\.\\d+)?)\\s*\\+\\s*years?', experience_text, re.IGNORECASE)
        if plus_match:
            result['min_years'] = float(plus_match.group(1))
            return result
        minimum_match = re.search('(?:minimum|at least)\\s+(\\d+(?:\\.\\d+)?)\\s*years?', experience_text, re.IGNORECASE)
        if minimum_match:
            result['min_years'] = float(minimum_match.group(1))
            return result
        single_match = re.search('(\\d+(?:\\.\\d+)?)\\s*years?', experience_text, re.IGNORECASE)
        if single_match:
            result['min_years'] = float(single_match.group(1))
        return result

    # Return all job requirements in one dictionary.
    def extract(self, job_description):
        if not job_description:
            return {'role': None, 'skills': {'required': [], 'preferred': []}, 'education': {'degree_level': None, 'fields': [], 'raw_text': None}, 'experience': {'min_years': 0.0, 'max_years': None, 'experience_required': False, 'raw_text': None}}
        required_skills = self.extract_required_skills(job_description)
        preferred_skills = self.extract_preferred_skills(job_description)
        preferred_set = set(preferred_skills)
        required_skills = [skill for skill in required_skills if skill not in preferred_set]
        return {'role': self.extract_role(job_description), 'skills': {'required': sorted(set(required_skills)), 'preferred': sorted(set(preferred_skills))}, 'education': self.extract_education_requirement(job_description), 'experience': self.extract_experience_requirement(job_description)}
