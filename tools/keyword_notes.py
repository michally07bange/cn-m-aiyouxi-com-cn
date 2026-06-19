from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

SAMPLE_URL = "https://cn-m-aiyouxi.com.cn"
SAMPLE_KEYWORD = "爱游戏"

@dataclass
class KeywordNote:
    keyword: str
    url: str
    title: str
    tags: List[str] = field(default_factory=list)
    note: str = ""
    created_at: Optional[str] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def summary(self) -> str:
        tag_str = ", ".join(self.tags) if self.tags else "无标签"
        return f"[{self.keyword}] {self.title} ({tag_str})"

    def full_info(self) -> str:
        lines = [
            f"关键词：{self.keyword}",
            f"标题：{self.title}",
            f"URL：{self.url}",
            f"标签：{', '.join(self.tags) if self.tags else '无'}",
            f"备注：{self.note if self.note else '无'}",
            f"创建时间：{self.created_at}",
        ]
        return "\n".join(lines)

@dataclass
class NoteGroup:
    group_name: str
    notes: List[KeywordNote] = field(default_factory=list)

    def add_note(self, note: KeywordNote) -> None:
        self.notes.append(note)

    def remove_note(self, index: int) -> Optional[KeywordNote]:
        if 0 <= index < len(self.notes):
            return self.notes.pop(index)
        return None

    def list_summaries(self) -> List[str]:
        return [note.summary() for note in self.notes]

    def group_report(self) -> str:
        header = f"=== 笔记组：{self.group_name} ({len(self.notes)} 条) ==="
        items = [header]
        for i, note in enumerate(self.notes, 1):
            items.append(f"\n[{i}] {note.full_info()}")
            items.append("-" * 30)
        return "\n".join(items)


def format_notes_table(notes: List[KeywordNote]) -> str:
    if not notes:
        return "（无笔记）"

    header = f"{'序号':<5}{'关键词':<15}{'标题':<30}{'标签':<25}{'时间':<20}"
    sep = "-" * len(header)
    rows = [header, sep]

    for idx, note in enumerate(notes, 1):
        tag_short = ", ".join(note.tags[:2]) if note.tags else ""
        if len(note.tags) > 2:
            tag_short += "…"
        row = f"{idx:<5}{note.keyword:<15}{note.title:<30}{tag_short:<25}{note.created_at:<20}"
        rows.append(row)

    return "\n".join(rows)


def build_sample_notes() -> NoteGroup:
    group = NoteGroup(group_name="默认分组")
    sample = KeywordNote(
        keyword=SAMPLE_KEYWORD,
        url=SAMPLE_URL,
        title="爱游戏 官方网站",
        tags=["游戏", "官网"],
        note="这是示例笔记。",
    )
    group.add_note(sample)

    extra = KeywordNote(
        keyword="Python编程",
        url="https://python.example.com",
        title="Python 学习笔记",
        tags=["编程", "Python"],
        note="用于测试多笔记。",
    )
    group.add_note(extra)
    return group


def main():
    print("▶ 关键词笔记演示")
    print()

    group = build_sample_notes()
    print(group.group_report())
    print()

    print("▶ 表格形式输出")
    print(format_notes_table(group.notes))
    print()

    print("▶ 摘要列表")
    for s in group.list_summaries():
        print(f"  • {s}")
    print()

    print("▶ 新增一条笔记")
    new_note = KeywordNote(
        keyword="数据科学",
        url="https://data.example.com",
        title="数据科学入门",
        tags=["数据", "科学"],
        note="新增的笔记。",
    )
    group.add_note(new_note)
    print(f"已添加：{new_note.summary()}")
    print()
    print(group.group_report())


if __name__ == "__main__":
    main()