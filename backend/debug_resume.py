#!/usr/bin/env python3

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.parsers.file_parser import extract_text
from app.parsers.section_detector import split_into_sections
from app.services.rule_based_extractor import extract_resume_data

def debug_resume_extraction(file_path=None):
    if file_path:
        print(f"=== DEBUGGING FILE: {file_path} ===")
        try:
            # Step 1: Extract raw text
            raw_text = extract_text(file_path)
            print(f"\n=== RAW TEXT (first 500 chars) ===")
            print(repr(raw_text[:500]))
            
            # Step 2: Split into sections
            sections = split_into_sections(raw_text)
            print(f"\n=== SECTIONS DETECTED ===")
            for key, value in sections.items():
                print(f"{key}: {repr(value[:100])}...")
            
            # Step 3: Extract structured data
            result = extract_resume_data(raw_text)
            print(f"\n=== STRUCTURED DATA ===")
            print(f"Name: {repr(result.get('name'))}")
            print(f"Email: {repr(result.get('email'))}")
            print(f"Phone: {repr(result.get('phone'))}")
            print(f"References present: {'references' in result}")
            if result.get('references'):
                print(f"References: {result['references']}")
            
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("Please provide a file path")
        print("Usage: python debug_resume.py <path_to_resume_file>")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        debug_resume_extraction(sys.argv[1])
    else:
        debug_resume_extraction()
