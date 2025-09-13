#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from datetime import datetime
import mysql.connector
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

class BoardDB:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        self.cur = self.conn.cursor(dictionary=True)

    def create_post(self, title, content):
        sql = "INSERT INTO posts (title, content) VALUES (%s, %s)"
        self.cur.execute(sql, (title, content))
        self.conn.commit()
        print("작성 완료.\n")

    def list_posts(self):
        self.cur.execute("SELECT * FROM posts ORDER BY id")
        rows = self.cur.fetchall()
        if not rows:
            print("\n[목록] 글이 없습니다.\n")
            return
        print("\n[목록]")
        for p in rows:
            print(f"- {p['id']:>3} | {p['title']} | {p['created_at']}")
        print()

    def view_post(self, pid):
        self.cur.execute("SELECT * FROM posts WHERE id=%s", (pid,))
        p = self.cur.fetchone()
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

    def update_post(self, pid, new_title, new_content):
        sql = "UPDATE posts SET title=%s, content=%s WHERE id=%s"
        self.cur.execute(sql, (new_title, new_content, pid))
        self.conn.commit()
        print("수정 완료.\n")

    def delete_post(self, pid):
        sql = "DELETE FROM posts WHERE id=%s"
        self.cur.execute(sql, (pid,))
        self.conn.commit()
        print("삭제 완료.\n")

    def close(self):
        self.cur.close()
        self.conn.close()


class Board:
    def __init__(self):
        self.db = BoardDB()

    def _multiline_input(self):
        print("내용 입력 (끝 입력 시 종료)")
        lines = []
        while True:
            line = input()
            if line.strip() == "끝":
                break
            lines.append(line)
        return "\n".join(lines).strip()

    def create_post(self):
        while True:
            title = input("\n[작성] 제목: ").strip()
            if title:
                break
            print("제목은 비울 수 없습니다.")

        while True:
            content = self._multiline_input()
            if content:
                break
            print("내용은 비울 수 없습니다. 다시 입력해주세요.")

        self.db.create_post(title, content)

    def list_posts(self):
        self.db.list_posts()

    def view_post(self):
        pid = input("조회할 ID: ").strip()
        if not pid.isdigit():
            print("ID는 숫자입니다.\n")
            return
        self.db.view_post(int(pid))

    def update_post(self):
        pid = input("수정할 ID: ").strip()
        if not pid.isdigit():
            print("ID는 숫자입니다.\n")
            return
        pid = int(pid)

        # 현재 글 가져오기
        self.db.cur.execute("SELECT * FROM posts WHERE id=%s", (pid,))
        cur = self.db.cur.fetchone()
        if not cur:
            print("해당 글이 없습니다.\n")
            return

        print(f"\n[수정] 현재 제목: {cur['title']}")
        new_title = input("새 제목(Enter면 유지): ").strip() or cur["title"]

        print("- 기존 내용 -")
        print(cur["content"])

        edit_content = input("내용을 수정하시겠습니까? (y/n): ").strip().lower()
        if edit_content == "y":
            print("- 새 내용 입력 (끝 입력 시 종료) -")
            new_content = self._multiline_input()
        else:
            new_content = cur["content"]

        self.db.update_post(pid, new_title, new_content)

    def delete_post(self):
        pid = input("삭제할 ID: ").strip()
        if not pid.isdigit():
            print("ID는 숫자입니다.\n")
            return
        self.db.delete_post(int(pid))

    def menu(self):
        print("""
[DB 기반 게시판]
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
                print("종료합니다.")
                self.db.close()
                break
            else:
                print("메뉴를 다시 선택하세요.\n")


def main():
    Board().run()

if __name__ == "__main__":
    main()