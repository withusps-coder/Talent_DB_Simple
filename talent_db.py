#!/usr/bin/env python3
"""
🚀 나만의 인재 DB 검색기
간단한 CRUD 테스트 프로젝트
"""

import json
import os
from datetime import datetime

# 데이터베이스 파일 경로
DB_FILE = "candidates.json"


def load_db():
    """데이터베이스 파일 로드"""
    if not os.path.exists(DB_FILE):
        return []
    
    try:
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []


def save_db(data):
    """데이터베이스 파일 저장"""
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("✅ 저장 완료!")


def add_candidate():
    """후보자 추가"""
    print("\n" + "="*50)
    print("📝 새 후보자 등록")
    print("="*50)
    
    name = input("이름: ").strip()
    contact = input("연락처: ").strip()
    skills = input("핵심 스킬 (쉼표로 구분): ").strip()
    experience = input("연차 (예: 3년): ").strip()
    
    if not name or not contact:
        print("❌ 이름과 연락처는 필수입니다!")
        return
    
    candidate = {
        "id": datetime.now().strftime("%Y%m%d%H%M%S"),
        "name": name,
        "contact": contact,
        "skills": skills,
        "experience": experience,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    db = load_db()
    db.append(candidate)
    save_db(db)
    
    print(f"\n✨ '{name}' 님이 등록되었습니다!")


def list_candidates():
    """후보자 목록 조회"""
    db = load_db()
    
    if not db:
        print("\n📭 등록된 후보자가 없습니다.")
        return
    
    print("\n" + "="*80)
    print(f"📋 전체 후보자 목록 ({len(db)}명)")
    print("="*80)
    
    for idx, candidate in enumerate(db, 1):
        print(f"\n[{idx}] {candidate['name']}")
        print(f"    📞 연락처: {candidate['contact']}")
        print(f"    💼 스킬: {candidate['skills']}")
        print(f"    📆 연차: {candidate['experience']}")
        print(f"    🕐 등록일: {candidate['created_at']}")
    
    print("\n" + "="*80)


def search_candidates():
    """후보자 검색"""
    keyword = input("\n🔍 검색어 (이름 또는 스킬): ").strip().lower()
    
    if not keyword:
        return
    
    db = load_db()
    results = [
        c for c in db 
        if keyword in c['name'].lower() or keyword in c['skills'].lower()
    ]
    
    if not results:
        print(f"\n❌ '{keyword}'에 대한 검색 결과가 없습니다.")
        return
    
    print("\n" + "="*80)
    print(f"🔍 검색 결과 ({len(results)}명)")
    print("="*80)
    
    for idx, candidate in enumerate(results, 1):
        print(f"\n[{idx}] {candidate['name']}")
        print(f"    📞 연락처: {candidate['contact']}")
        print(f"    💼 스킬: {candidate['skills']}")
        print(f"    📆 연차: {candidate['experience']}")
    
    print("\n" + "="*80)


def show_menu():
    """메뉴 표시"""
    print("\n" + "="*50)
    print("🎯 인재 DB 검색기")
    print("="*50)
    print("1. 📝 후보자 등록")
    print("2. 📋 전체 목록 조회")
    print("3. 🔍 후보자 검색")
    print("4. 🚪 종료")
    print("="*50)


def main():
    """메인 함수"""
    print("\n🚀 나만의 인재 DB 검색기 v1.0")
    
    while True:
        show_menu()
        choice = input("\n선택 (1-4): ").strip()
        
        if choice == '1':
            add_candidate()
        elif choice == '2':
            list_candidates()
        elif choice == '3':
            search_candidates()
        elif choice == '4':
            print("\n👋 프로그램을 종료합니다.")
            break
        else:
            print("\n❌ 올바른 번호를 입력하세요 (1-4)")


if __name__ == "__main__":
    main()
