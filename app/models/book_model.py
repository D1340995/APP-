import sqlite3
import os

# 設定資料庫路徑，對應到 instance/database.db
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'instance', 'database.db')

def get_db_connection():
    """取得資料庫連線"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # 讓查詢結果能以字典形式存取
    return conn

def init_db():
    """初始化資料庫（執行 schema.sql）"""
    schema_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'database', 'schema.sql')
    if not os.path.exists(schema_path):
        return
        
    conn = get_db_connection()
    with open(schema_path, 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()

def create_book(title, review='', rating=0, is_favorite=0):
    """新增一本書籍紀錄"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO books (title, review, rating, is_favorite) VALUES (?, ?, ?, ?)',
        (title, review, rating, is_favorite)
    )
    conn.commit()
    conn.close()

def get_all_books():
    """取得所有書籍紀錄"""
    conn = get_db_connection()
    books = conn.execute('SELECT * FROM books ORDER BY created_at DESC').fetchall()
    conn.close()
    return [dict(book) for book in books]

def get_book_by_id(book_id):
    """根據 ID 取得單一書籍"""
    conn = get_db_connection()
    book = conn.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()
    conn.close()
    return dict(book) if book else None

def update_book(book_id, title, review, rating, is_favorite):
    """更新書籍資料"""
    conn = get_db_connection()
    conn.execute(
        'UPDATE books SET title = ?, review = ?, rating = ?, is_favorite = ? WHERE id = ?',
        (title, review, rating, is_favorite, book_id)
    )
    conn.commit()
    conn.close()

def delete_book(book_id):
    """刪除書籍"""
    conn = get_db_connection()
    conn.execute('DELETE FROM books WHERE id = ?', (book_id,))
    conn.commit()
    conn.close()

def search_books(keyword):
    """關鍵字搜尋（書名或心得）"""
    conn = get_db_connection()
    search_term = f'%{keyword}%'
    books = conn.execute(
        'SELECT * FROM books WHERE title LIKE ? OR review LIKE ? ORDER BY created_at DESC',
        (search_term, search_term)
    ).fetchall()
    conn.close()
    return [dict(book) for book in books]

def toggle_favorite(book_id):
    """切換收藏狀態"""
    book = get_book_by_id(book_id)
    if book:
        new_status = 1 if book['is_favorite'] == 0 else 0
        conn = get_db_connection()
        conn.execute('UPDATE books SET is_favorite = ? WHERE id = ?', (new_status, book_id))
        conn.commit()
        conn.close()
