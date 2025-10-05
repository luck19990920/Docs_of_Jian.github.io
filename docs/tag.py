import re
import yaml
from pathlib import Path

d = {}      # 键为categories，值为[title, path]   
path_relative = Path(r"C:\Users\89732\Desktop\web\mkdocs-blog-starter-project\Docs_of_Jian.github.io\docs")
path_blog = Path(r"C:\Users\89732\Desktop\web\mkdocs-blog-starter-project\Docs_of_Jian.github.io\docs\blog\posts")
path_tag = Path(r"C:\Users\89732\Desktop\web\mkdocs-blog-starter-project\Docs_of_Jian.github.io\docs\tag.md")

def read_yaml(path: Path):
    # 从单个文件中提取出yaml的部分，并且返回categories与title这两部分
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    pattern = r"---\n([\s\S]+)\n---"
    result = re.match(pattern, content)
    if result is None:
        return 
    pattern_result = result.group(1)
    try:
        categories = yaml.safe_load(pattern_result)["categories"]
        title = yaml.safe_load(pattern_result)["title"]
    except:
        return 
    
    global d
    for c in categories:
        if c in list(d.keys()):
            d.get(c).append([title, path.relative_to(path_relative)]) # type: ignore
        else:
            d[c] = [[title, path.relative_to(path_relative)]]


def write_yaml(path: Path):
    with open(path, "a", encoding="utf-8") as f:
        for k in list(d.keys()):
            f.write(f"\n## {k}\n\n")
            for v in d[k]:
                f.write(f'* [{v[0]}]({".\\"+str(v[1])})\n')


for md_file in path_blog.rglob("*.md"):
    read_yaml(md_file)

write_yaml(path_tag)











