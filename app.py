#!/usr/bin/env python3
"""
🌐 나만의 인재 DB 검색기 - 웹 버전
Flask 백엔드 서버
"""

from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)
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


@app.route('/')
def index():
    """메인 페이지"""
    return render_template('index.html')


@app.route('/api/candidates', methods=['GET'])
def get_candidates():
    """전체 후보자 목록 조회"""
    db = load_db()
    return jsonify(db)


@app.route('/api/candidates', methods=['POST'])
def add_candidate():
    """후보자 추가"""
    data = request.json
    
    candidate = {
        "id": datetime.now().strftime("%Y%m%d%H%M%S%f"),
        "name": data.get('name', '').strip(),
        "contact": data.get('contact', '').strip(),
        "skills": data.get('skills', '').strip(),
        "experience": data.get('experience', '').strip(),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    if not candidate['name'] or not candidate['contact']:
        return jsonify({"error": "이름과 연락처는 필수입니다"}), 400
    
    db = load_db()
    db.append(candidate)
    save_db(db)
    
    return jsonify({"message": "등록 완료!", "candidate": candidate}), 201


@app.route('/api/candidates/search', methods=['GET'])
def search_candidates():
    """후보자 검색"""
    keyword = request.args.get('keyword', '').strip().lower()
    
    if not keyword:
        return jsonify([])
    
    db = load_db()
    results = [
        c for c in db 
        if keyword in c['name'].lower() or keyword in c['skills'].lower()
    ]
    
    return jsonify(results)


@app.route('/api/candidates/<candidate_id>', methods=['DELETE'])
def delete_candidate(candidate_id):
    """후보자 삭제"""
    db = load_db()
    db = [c for c in db if c['id'] != candidate_id]
    save_db(db)
    
    return jsonify({"message": "삭제 완료!"}), 200


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 인재 DB 검색기 웹 서버 시작!")
    print("="*60)
    print("📍 주소: http://localhost:5000")
    print("🌐 브라우저에서 위 주소로 접속하세요!")
    print("⏹️  종료: Ctrl+C")
    print("="*60 + "\n")
    
    app.run(debug=True, port=5000)
