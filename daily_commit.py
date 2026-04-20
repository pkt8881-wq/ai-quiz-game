# -*- coding: utf-8 -*-
"""
매일 실행: 문제 50개 생성 + GitHub 자동 커밋
"""
import os, subprocess, sys
from datetime import datetime

BASE = os.path.dirname(__file__)

def run(cmd, **kw):
    return subprocess.run(cmd, shell=True, cwd=BASE, capture_output=True, text=True, **kw)

print("=== AI 퀴즈게임 일일 업데이트 ===")
print(f"날짜: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

# 1. 문제 생성
print("\n[1/3] 미로로 문제 50개 생성 중...")
result = subprocess.run(
    [sys.executable, os.path.join(BASE, 'daily_gen.py')],
    cwd=BASE, text=True, encoding='utf-8', errors='replace'
)
print(result.stdout[-500:] if result.stdout else "출력 없음")

# 2. 문제 수 집계
import json, glob
total = 0
counts = {}
for f in sorted(glob.glob(os.path.join(BASE, 'questions', '*.json'))):
    name = os.path.basename(f).replace('.json','')
    data = json.load(open(f, encoding='utf-8'))
    counts[name] = len(data)
    total += len(data)

summary = ', '.join(f"{k}:{v}" for k,v in counts.items())
print(f"\n총 문제: {total}개 ({summary})")

# 3. GitHub 커밋 & 푸시
print("\n[2/3] GitHub 커밋 중...")
today = datetime.now().strftime('%Y-%m-%d')

run('git add questions/')
commit_msg = f"daily: {today} 문제 업데이트 (총 {total}개)"
r = run(f'git commit -m "{commit_msg}"')
if 'nothing to commit' in r.stdout + r.stderr:
    print("변경사항 없음 - 커밋 스킵")
else:
    print(r.stdout or r.stderr)
    push = run('git push origin main')
    print("[3/3] 푸시 완료!" if push.returncode == 0 else f"푸시 오류: {push.stderr}")

print("\n=== 완료 ===")
