from pathlib import Path
from database import conn

# 1 - Obtemos os posts do banco de dados e deserializamos em um dict
cursor = conn.cursor()
fields = ("id", "title", "content", "author")
results = cursor.execute(f"SELECT * FROM post;")
posts = [dict(zip(fields, post)) for post in results]

# 2 - Criamos a pasta de destino do site
site_dir = Path("site")
site_dir.mkdir(exist_ok=True)

# 3 - Criamos uma função capaz de gerar a url de um post
def get_post_url(post):
    slug = post["title"].lower().replace(" ", "-")
    return f"{slug}.html"


# 3 - Renderizamos o a página `index.html` a partir do template.
index_template = Path("list.template.html").read_text()
index_page = site_dir / Path("index.html")
post_list = [
    f"<li><a href='{get_post_url(post)}'>{post['title']}</a></li>"
    for post in posts
]
index_page.write_text(
    index_template.format(post_list="\n".join(post_list))
)

# 4 - Renderizamos todas as páginas para cada post  partir do template.
for post in posts:
    post_template = Path("post.template.html").read_text()
    post_page = site_dir / Path(get_post_url(post))
    post_page.write_text(post_template.format(post=post))

print("Site generated at", site_dir)

# 5 - fechamos a conexão
conn.close()
