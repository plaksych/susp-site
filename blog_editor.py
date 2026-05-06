import tkinter as tk
from tkinter import filedialog, messagebox
import shutil, os, re, subprocess
from datetime import datetime

SCRIPT_DIR   = os.path.dirname(os.path.abspath(__file__))
BLOG_HTML    = os.path.join(SCRIPT_DIR, "pages", "blog.html")
IMAGES_DIR   = os.path.join(SCRIPT_DIR, "assets", "images", "blog")
START_MARKER = "<!-- BLOG_POSTS_START -->"


def ensure_images_dir():
    os.makedirs(IMAGES_DIR, exist_ok=True)


def read_html():
    with open(BLOG_HTML, "r", encoding="utf-8") as f:
        return f.read()


def write_html(content):
    with open(BLOG_HTML, "w", encoding="utf-8") as f:
        f.write(content)


def build_post_html(author, date, text, img_rel=None):
    img_html = ""
    if img_rel:
        img_html = '          <img src="' + img_rel + '" alt="post image" class="blog-post-image" />\n'
    escaped  = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    divider  = "&#9604;&#9600;&#9608;" * 12
    return (
        '        <article class="blog-post">\n'
        '          <div class="blog-post-header">\n'
        '            <span class="blog-post-author">&#9733; ' + author + '</span>\n'
        '            <span class="blog-post-date">' + date + '</span>\n'
        '          </div>\n'
        + img_html
        + '          <p class="blog-post-text">' + escaped + '</p>\n'
        '        </article>\n'
        '        <p class="section-divider">' + divider + '</p>\n'
    )


def insert_post(author, date, text, img_path=None):
    ensure_images_dir()
    img_rel = None
    if img_path:
        filename = os.path.basename(img_path)
        dest = os.path.join(IMAGES_DIR, filename)
        if os.path.abspath(img_path) != os.path.abspath(dest):
            base, ext = os.path.splitext(filename)
            n = 1
            while os.path.exists(dest):
                dest = os.path.join(IMAGES_DIR, base + "_" + str(n) + ext)
                n += 1
            shutil.copy2(img_path, dest)
        img_rel = "../assets/images/blog/" + os.path.basename(dest)
    html = read_html()
    write_html(html.replace(START_MARKER, START_MARKER + "\n" + build_post_html(author, date, text, img_rel)))


def load_posts():
    html = read_html()
    pat = re.compile(
        r'<span class="blog-post-author">&#9733; (.*?)</span>.*?'
        r'<span class="blog-post-date">(.*?)</span>',
        re.DOTALL)
    return [(m.group(1).strip(), m.group(2).strip()) for m in pat.finditer(html)]


def delete_post(index):
    html = read_html()
    # каждый пост = <article ...> ... </article>\n + divider\n
    pat = re.compile(
        r'        <article class="blog-post">.*?</article>\n'
        r'        <p class="section-divider">.*?</p>\n',
        re.DOTALL)
    matches = list(pat.finditer(html))
    if index < 0 or index >= len(matches):
        raise IndexError("Пост не найден")
    m = matches[index]
    write_html(html[:m.start()] + html[m.end():])


# ── GUI ────────────────────────────────────────────────────────────────────

class BlogEditor(tk.Tk):
    BG   = "#0d0000"; BG2  = "#1a0000"; RED  = "#ff0000"
    ORA  = "#ff6600"; GRN  = "#00ff00"; GREY = "#cccccc"; DARK = "#444444"
    FONT = ("Verdana", 10); FONTS = ("Verdana", 9); MONO = ("Courier New", 10)

    def __init__(self):
        super().__init__()
        self.title("Suspiria — Blog Editor")
        self.configure(bg=self.BG)
        self.resizable(False, False)
        self.selected_image = tk.StringVar()
        self._build_ui()
        self._refresh_list()

    def _lbl(self, parent, text, c=None, f=None):
        return tk.Label(parent, text=text, bg=self.BG, fg=c or self.GREY, font=f or self.FONT)

    def _build_ui(self):
        tk.Label(self, text="★ SUSPIRIA BLOG EDITOR ★",
                 bg=self.BG, fg=self.RED, font=("Impact", 20)).pack(pady=(14, 2))
        tk.Label(self, text="── создать новый пост ──",
                 bg=self.BG, fg=self.DARK, font=self.FONTS).pack()

        form = tk.Frame(self, bg=self.BG, padx=18, pady=10)
        form.pack(fill="x")
        p = {"pady": 5, "padx": (8, 0)}

        # Автор
        self._lbl(form, "Автор:").grid(row=0, column=0, sticky="w", pady=5)
        self.author_var = tk.StringVar()
        tk.Entry(form, textvariable=self.author_var, width=34,
                 bg=self.BG2, fg=self.ORA, insertbackground=self.ORA,
                 relief="flat", highlightthickness=1,
                 highlightbackground=self.RED, highlightcolor=self.RED,
                 font=self.FONT).grid(row=0, column=1, sticky="w", **p)

        # Дата
        self._lbl(form, "Дата:").grid(row=1, column=0, sticky="w", pady=5)
        self.date_var = tk.StringVar(value=datetime.now().strftime("%d.%m.%Y"))
        tk.Entry(form, textvariable=self.date_var, width=16,
                 bg=self.BG2, fg=self.GREY, insertbackground=self.GREY,
                 relief="flat", highlightthickness=1,
                 highlightbackground=self.RED, highlightcolor=self.RED,
                 font=self.MONO).grid(row=1, column=1, sticky="w", **p)

        # Картинка
        self._lbl(form, "Картинка:").grid(row=2, column=0, sticky="w", pady=5)
        row2 = tk.Frame(form, bg=self.BG)
        row2.grid(row=2, column=1, sticky="w", **p)
        self.img_label = tk.Label(row2, text="не выбрана",
                                  bg=self.BG, fg=self.DARK, font=self.FONTS)
        self.img_label.pack(side="left")
        tk.Button(row2, text="[ выбрать ]", bg=self.BG2, fg=self.GRN,
                  activebackground=self.GRN, activeforeground="#000",
                  relief="flat", font=self.FONT, cursor="hand2",
                  command=self._pick_image).pack(side="left", padx=(8, 0))
        tk.Button(row2, text="[ x ]", bg=self.BG2, fg=self.RED,
                  activebackground=self.RED, activeforeground="#000",
                  relief="flat", font=self.FONT, cursor="hand2",
                  command=self._clear_image).pack(side="left", padx=(4, 0))

        # Текст
        self._lbl(form, "Текст:").grid(row=3, column=0, sticky="nw", pady=5)
        self.text_box = tk.Text(form, width=44, height=7,
                                bg=self.BG2, fg=self.GREY, insertbackground=self.GREY,
                                relief="flat", highlightthickness=1,
                                highlightbackground=self.RED, highlightcolor=self.RED,
                                font=self.FONT, wrap="word")
        self.text_box.grid(row=3, column=1, sticky="w", **p)

        # Кнопка публикации
        tk.Button(self, text="[ ★ ОПУБЛИКОВАТЬ ПОСТ ★ ]",
                  bg="#001a00", fg=self.GRN,
                  activebackground=self.GRN, activeforeground="#000",
                  relief="flat", font=("Courier New", 12, "bold"),
                  cursor="hand2", pady=8,
                  command=self._submit).pack(fill="x", padx=18, pady=(4, 12))

        # Список постов
        tk.Label(self, text="── опубликованные посты ──",
                 bg=self.BG, fg=self.DARK, font=self.FONTS).pack()
        lf = tk.Frame(self, bg=self.BG, padx=18, pady=8)
        lf.pack(fill="both")
        self.post_list = tk.Listbox(lf, width=52, height=6,
                                    bg=self.BG2, fg=self.GREY,
                                    selectbackground="#330000", selectforeground=self.RED,
                                    relief="flat", highlightthickness=1,
                                    highlightbackground=self.RED, font=self.MONO)
        self.post_list.pack(side="left", fill="both", expand=True)
        sb = tk.Scrollbar(lf, command=self.post_list.yview, bg=self.BG2)
        sb.pack(side="right", fill="y")
        self.post_list.config(yscrollcommand=sb.set)

        tk.Label(self, bg=self.BG, fg=self.DARK, font=("Verdana", 8),
                 text="посты добавляются сверху в pages/blog.html").pack(pady=(0, 4))

        # Удалить пост
        tk.Button(self, text="[ ✕ УДАЛИТЬ ВЫБРАННЫЙ ПОСТ ]",
                  bg=self.BG2, fg=self.RED,
                  activebackground=self.RED, activeforeground="#000",
                  relief="flat", font=("Courier New", 10, "bold"),
                  cursor="hand2", pady=5,
                  command=self._delete_post).pack(fill="x", padx=18, pady=(0, 6))

        # Git push
        tk.Button(self, text="[ ↑ GIT PUSH ]",
                  bg="#00001a", fg="#6666ff",
                  activebackground="#6666ff", activeforeground="#000",
                  relief="flat", font=("Courier New", 11, "bold"),
                  cursor="hand2", pady=6,
                  command=self._git_push).pack(fill="x", padx=18, pady=(0, 12))

    def _pick_image(self):
        path = filedialog.askopenfilename(
            title="Выбери картинку",
            filetypes=[("Изображения", "*.jpg *.jpeg *.png *.gif *.webp")])
        if path:
            self.selected_image.set(path)
            self.img_label.config(text=os.path.basename(path), fg=self.GRN)

    def _clear_image(self):
        self.selected_image.set("")
        self.img_label.config(text="не выбрана", fg=self.DARK)

    def _submit(self):
        author = self.author_var.get().strip()
        date   = self.date_var.get().strip()
        text   = self.text_box.get("1.0", "end").strip()
        img    = self.selected_image.get()
        if not author:
            messagebox.showerror("Ошибка", "Укажи автора!"); return
        if not text:
            messagebox.showerror("Ошибка", "Текст поста пустой!"); return
        if not messagebox.askyesno("Подтверждение", "Опубликовать пост?"):
            return
        try:
            insert_post(author, date, text, img or None)
        except Exception as e:
            messagebox.showerror("Ошибка", str(e)); return
        messagebox.showinfo("Готово", "Пост опубликован в blog.html!")
        self.text_box.delete("1.0", "end")
        self._clear_image()
        self._refresh_list()

    def _delete_post(self):
        sel = self.post_list.curselection()
        if not sel:
            messagebox.showwarning("Удаление", "Сначала выбери пост из списка."); return
        idx = sel[0]
        entry = self.post_list.get(idx).strip()
        if not messagebox.askyesno("Удаление", "Удалить пост?\n\n" + entry):
            return
        try:
            delete_post(idx)
        except Exception as e:
            messagebox.showerror("Ошибка", str(e)); return
        messagebox.showinfo("Готово", "Пост удалён.")
        self._refresh_list()

    def _git_push(self):
        if not messagebox.askyesno("Git Push", "Запушить все изменения на сайте?\n\nКоммит: \"blog post update\""):
            return
        try:
            result = subprocess.run(
                ["git", "add", "-A"],
                cwd=SCRIPT_DIR, capture_output=True, text=True)
            if result.returncode != 0:
                messagebox.showerror("Git error", "git add:\n" + result.stderr); return

            result = subprocess.run(
                ["git", "commit", "-m", "blog post update"],
                cwd=SCRIPT_DIR, capture_output=True, text=True)
            if result.returncode != 0 and "nothing to commit" not in result.stdout:
                messagebox.showerror("Git error", "git commit:\n" + result.stderr); return

            result = subprocess.run(
                ["git", "push"],
                cwd=SCRIPT_DIR, capture_output=True, text=True)
            if result.returncode != 0:
                messagebox.showerror("Git error", "git push:\n" + result.stderr); return

            messagebox.showinfo("Git Push", "Готово! Изменения запушены.")
        except FileNotFoundError:
            messagebox.showerror("Ошибка", "Git не найден. Убедись что git установлен и доступен в PATH.")

    def _refresh_list(self):
        self.post_list.delete(0, "end")
        try:
            posts = load_posts()
        except Exception:
            return
        if not posts:
            self.post_list.insert("end", "  (постов пока нет)")
            return
        for author, date in posts:
            self.post_list.insert("end", "  " + date + "  —  " + author)


if __name__ == "__main__":
    BlogEditor().mainloop()
