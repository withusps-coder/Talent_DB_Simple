// 페이지 로드 시 후보자 목록 불러오기
document.addEventListener('DOMContentLoaded', function () {
    loadCandidates();
});

// 후보자 목록 불러오기
async function loadCandidates() {
    try {
        const response = await fetch('/api/candidates');
        const candidates = await response.json();

        displayCandidates(candidates);
        updateStats(candidates);

        // 검색창 초기화
        document.getElementById('searchInput').value = '';
    } catch (error) {
        showToast('목록을 불러오는데 실패했습니다.', 'error');
    }
}

// 후보자 추가
async function addCandidate(event) {
    event.preventDefault();

    const candidate = {
        name: document.getElementById('name').value,
        contact: document.getElementById('contact').value,
        skills: document.getElementById('skills').value,
        experience: document.getElementById('experience').value
    };

    try {
        const response = await fetch('/api/candidates', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(candidate)
        });

        if (response.ok) {
            showToast(`✨ '${candidate.name}' 님이 등록되었습니다!`, 'success');
            document.getElementById('candidateForm').reset();
            loadCandidates();
        } else {
            const error = await response.json();
            showToast(error.error || '등록에 실패했습니다.', 'error');
        }
    } catch (error) {
        showToast('등록에 실패했습니다.', 'error');
    }
}

// 후보자 검색
async function searchCandidates() {
    const keyword = document.getElementById('searchInput').value.trim();

    if (!keyword) {
        loadCandidates();
        return;
    }

    try {
        const response = await fetch(`/api/candidates/search?keyword=${encodeURIComponent(keyword)}`);
        const candidates = await response.json();

        displayCandidates(candidates);
        updateStats(candidates);

        if (candidates.length === 0) {
            showToast(`'${keyword}'에 대한 검색 결과가 없습니다.`, 'error');
        } else {
            showToast(`${candidates.length}명의 후보자를 찾았습니다.`, 'success');
        }
    } catch (error) {
        showToast('검색에 실패했습니다.', 'error');
    }
}

// 후보자 삭제
async function deleteCandidate(id, name) {
    if (!confirm(`'${name}' 님을 정말 삭제하시겠습니까?`)) {
        return;
    }

    try {
        const response = await fetch(`/api/candidates/${id}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            showToast(`'${name}' 님이 삭제되었습니다.`, 'success');
            loadCandidates();
        } else {
            showToast('삭제에 실패했습니다.', 'error');
        }
    } catch (error) {
        showToast('삭제에 실패했습니다.', 'error');
    }
}

// 후보자 표시
function displayCandidates(candidates) {
    const listElement = document.getElementById('candidateList');

    if (candidates.length === 0) {
        listElement.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">📭</div>
                <p>등록된 후보자가 없습니다.</p>
                <p style="font-size: 0.9rem; margin-top: 10px;">위 폼에서 새 후보자를 등록해보세요!</p>
            </div>
        `;
        return;
    }

    listElement.innerHTML = candidates.map(candidate => `
        <div class="candidate-card">
            <div class="candidate-header">
                <div class="candidate-name">${candidate.name}</div>
                <button class="btn-delete" onclick="deleteCandidate('${candidate.id}', '${candidate.name}')">
                    🗑️ 삭제
                </button>
            </div>
            <div class="candidate-info">
                <div class="info-row">
                    <span class="info-label">📞 연락처:</span>
                    <span>${candidate.contact}</span>
                </div>
                ${candidate.skills ? `
                <div class="info-row">
                    <span class="info-label">💼 스킬:</span>
                    <span>${candidate.skills}</span>
                </div>
                ` : ''}
                ${candidate.experience ? `
                <div class="info-row">
                    <span class="info-label">📆 연차:</span>
                    <span>${candidate.experience}</span>
                </div>
                ` : ''}
                <div class="info-row">
                    <span class="info-label">🕐 등록일:</span>
                    <span>${candidate.created_at}</span>
                </div>
            </div>
        </div>
    `).join('');
}

// 통계 업데이트
function updateStats(candidates) {
    document.getElementById('totalCount').textContent = candidates.length;
}

// 토스트 알림
function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast ${type} show`;

    setTimeout(() => {
        toast.className = 'toast';
    }, 3000);
}

// 검색창에서 엔터키 입력 시 검색
document.getElementById('searchInput').addEventListener('keypress', function (event) {
    if (event.key === 'Enter') {
        searchCandidates();
    }
});
