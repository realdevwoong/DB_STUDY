#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime

class Board:
    def __init__(self):
        self.posts = []   # {"id":int, "title":str, "content":str, "created_at":str}
        self.seq = 0

    # 내부용: 여러 줄 입력 (끝 입력 시 종료)
    def _multiline_input(self):
        print("내용 입력 (끝 입력 시 종료)")
        lines = []
        while True:
            line = input()
            if line.strip() == "끝":
                break
            lines.append(line)
        return "\n".join(lines).strip()

    # C
    def create_post(self):
        # 제목 입력 (비울 수 없음)
        while True:
            title = input("\n[작성] 제목: ").strip()
            if title:
                break
            print("제목은 비울 수 없습니다.")
        
        # 내용 입력 (비울 수 없음)
        while True:
            content = self._multiline_input()
            if content:
                break
            print("내용은 비울 수 없습니다. 다시 입력해주세요.")

        self.seq += 1
        self.posts.append({
            "id": self.seq,
            "title": title,
            "content": content,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        })
        print("작성 완료.\n")

    # R - 목록
    def list_posts(self):
        if not self.posts:
            print("\n[목록] 글이 없습니다.\n")
            return
        print("\n[목록]")
        for p in sorted(self.posts, key=lambda x: x["id"]):  # 오래된 → 최신
            print(f"- {p['id']:>3} | {p['title']} | {p['created_at']}")
        print()

    # R - 상세
    def view_post(self):
        pid = input("조회할 ID: ").strip()
        if not pid.isdigit():
            print("ID는 숫자입니다.\n")
            return
        pid = int(pid)
        p = next((x for x in self.posts if x["id"] == pid), None)
        if not p:
            print("해당 글이 없습니다.\n")
            return
        print("\n[상세]")
        print(f"ID: {p['id']}")
        print(f"제목: {p['title']}")
        print(f"작성일: {p['created_at']}")
        print("-"*40)
        print(p["content"])
        print()

    # U
    # U
    def update_post(self):
        pid = input("수정할 ID: ").strip()
        if not pid.isdigit():
            print("ID는 숫자입니다.\n")
            return
        pid = int(pid)
        idx = next((i for i, x in enumerate(self.posts) if x["id"] == pid), -1)
        if idx < 0:
            print("해당 글이 없습니다.\n")
            return
        
        cur = self.posts[idx]
        print(f"\n[수정] 현재 제목: {cur['title']}")
        new_title = input("새 제목(Enter면 유지): ").strip() or cur["title"]
        
        print("- 기존 내용 -")
        print(cur["content"])
        
        # 먼저 내용 수정 여부 확인
        edit_content = input("내용을 수정하시겠습니까? (y/n): ").strip().lower()
        
        if edit_content == 'y':
            print("- 새 내용 입력 (끝 입력 시 종료) -")
            new_content = self._multiline_input()
        else:
            new_content = cur["content"]
        
        cur["title"] = new_title
        cur["content"] = new_content
        print("수정 완료.\n")

    # D
    def delete_post(self):
        pid = input("삭제할 ID: ").strip()
        if not pid.isdigit():
            print("ID는 숫자입니다.\n")
            return
        pid = int(pid)

        before = len(self.posts)
        self.posts = [p for p in self.posts if p["id"] != pid]
        if len(self.posts) == before:
            print("삭제 대상이 없습니다.\n")
            return
        print("삭제 완료.\n")

    def menu(self):
        print("""
[메모리 기반 게시판]
1) 목록
2) 상세
3) 작성
4) 수정
5) 삭제
0) 종료
""")

    def run(self):
        while True:
            self.menu()
            choice = input("선택: ").strip()
            if choice == "1": self.list_posts()
            elif choice == "2": self.view_post()
            elif choice == "3": self.create_post()
            elif choice == "4": self.update_post()
            elif choice == "5": self.delete_post()
            elif choice == "0":
                print("종료합니다."); break
            else:
                print("메뉴를 다시 선택하세요.\n")

def main():
    Board().run()

if __name__ == "__main__":
    main()