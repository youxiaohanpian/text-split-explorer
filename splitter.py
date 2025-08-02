import streamlit as st
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter, Language
import code_snippets as code_snippets
import tiktoken
import csv
import io

# Streamlit UI
st.title("文本分割器")
st.info("""使用**文本分割器**将文本分割成块。参数包括：

- `chunk_size`：生成的块的最大大小（以所选的字符或标记为单位）
- `chunk_overlap`：生成的块之间的重叠部分（以所选的字符或标记为单位）
- `length_function`：如何测量块的长度，包含以字符或标记为单位的示例
- 文本分割器的类型，这在很大程度上控制了用于分割的分隔符
""")
col1, col2, col3, col4 = st.columns([1, 1, 1, 2])

with col1:
    chunk_size = st.number_input(min_value=1, label="Chunk Size", value=1000)

with col2:
    # Setting the max value of chunk_overlap based on chunk_size
    chunk_overlap = st.number_input(
        min_value=1,
        max_value=chunk_size - 1,
        label="Chunk Overlap",
        value=int(chunk_size * 0.2),
    )

    # Display a warning if chunk_overlap is not less than chunk_size
    if chunk_overlap >= chunk_size:
        st.warning("Chunk Overlap should be less than Chunk Length!")

with col3:
    length_function = st.selectbox(
        "Length Function", ["Characters", "Tokens"]
    )

splitter_choices = ["RecursiveCharacter", "Character"] + [str(v) for v in Language]

with col4:
    splitter_choice = st.selectbox(
        "Select a Text Splitter", splitter_choices
    )

if length_function == "Characters":
    length_function = len
    length_function_str = code_snippets.CHARACTER_LENGTH
elif length_function == "Tokens":
    enc = tiktoken.get_encoding("cl100k_base")

    def length_function(text: str) -> int:
        return len(enc.encode(text))

    length_function_str = code_snippets.TOKEN_LENGTH
else:
    raise ValueError

if splitter_choice == "Character":
    import_text = code_snippets.CHARACTER.format(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=length_function_str
    )
elif splitter_choice == "RecursiveCharacter":
    import_text = code_snippets.RECURSIVE_CHARACTER.format(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=length_function_str
    )
elif "Language." in splitter_choice:
    import_text = code_snippets.LANGUAGE.format(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        language=splitter_choice,
        length_function=length_function_str
    )
else:
    raise ValueError

st.info(import_text)

# Box for pasting text
doc = st.text_area("粘贴文本:")

# Split text button
if st.button("分割"):
    # Choose splitter and initialize it
    if splitter_choice == "Character":
        splitter = CharacterTextSplitter(
            separator="\n\n",
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=length_function
        )
    elif splitter_choice == "RecursiveCharacter":
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=length_function
        )
    elif "Language." in splitter_choice:
        language = splitter_choice.split(".")[1].lower()
        splitter = RecursiveCharacterTextSplitter.from_language(
            language,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=length_function
        )
    else:
        raise ValueError

    # Split the text
    splits = splitter.split_text(doc)

    # Display the splits
    for idx, split in enumerate(splits, start=1):
        st.text_area(f"分割部分 {idx}", split, height=200)

    # Export CSV
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Page", "Text"])
    for i, chunk in enumerate(splits, 1):
        writer.writerow([i, chunk])

    csv_data = output.getvalue()
    output.close()

    # Add BOM for UTF-8 to ensure Chinese characters display correctly in Excel
    csv_data_with_bom = '\ufeff' + csv_data

    st.download_button(
        label="下载 CSV",
        data=csv_data_with_bom,
        file_name="splits.csv",
        mime="text/csv"
    )
