with open('article.html', 'r', encoding='utf-8') as f:
    text = f.read()

bad_orphan = """  }


    if (fit === '16-9-crop') {
      return 'width:100%; aspect-ratio:16/9; object-fit:cover; object-position:' + pos + '; display:block;';
    }
    if (fit === '4-3' || fit === '4:3') {
      return 'width:100%; aspect-ratio:4/3; object-fit:contain; object-position:' + pos + '; background:#050505; display:block;';
    }
    if (fit === '1-1' || fit === '1:1') {
      return 'max-width:550px; width:100%; aspect-ratio:1/1; object-fit:contain; object-position:' + pos + '; margin:0 auto; display:block;';
    }
    if (fit === 'cover') {
      return 'width:100%; max-height:550px; object-fit:cover; object-position:' + pos + '; display:block;';
    }
    return 'width:100%; max-height:650px; object-fit:contain; object-position:' + pos + '; background:#050505; display:block;';
  }"""

clean_orphan = """  }"""

norm_text = text.replace('\r\n', '\n')
norm_bad = bad_orphan.replace('\r\n', '\n')
norm_clean = clean_orphan.replace('\r\n', '\n')

if norm_bad in norm_text:
    new_text = norm_text.replace(norm_bad, norm_clean, 1)
    with open('article.html', 'w', encoding='utf-8', newline='\r\n') as f:
        f.write(new_text)
    print("SUCCESS: Orphan block removed!")
else:
    print("ERROR: Orphan block not matched exactly.")

