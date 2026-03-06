import re

if __name__ == "__main__":
    file_path = "junk"
    with open(file_path, "r") as file:
        content = file.read()
        # Find all sequences of consecutive literal '\n' (backslash followed by n)
        figure_matches = re.findall(r"((?:\\n)+Figure)", content)
        if figure_matches:
            print("AAAAAAAAAA: ", figure_matches)

        chapter_matches = re.findall(r"((?:\\n){3,}\w)", content)
        if chapter_matches:
            print("BBBBBBBB: ", chapter_matches)
