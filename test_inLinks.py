def create_in_links(out_links_dic):
    in_links = dict()
    N = len(out_links_dic.keys())
    for main_page in out_links_dic.keys():
        in_links[main_page] = [page for page in out_links_dic.keys() if
                               main_page in out_links_dic[page] and page != main_page]
    old_PR = {page_name: 1 for page_name in out_links_dic.keys()}
    new_PR = {page_name: 0 for page_name in out_links_dic.keys()}
    dampping_factor = 0.85
    difference = sum([abs(old_PR[page_name]-new_PR[page_name]) for page_name in out_links_dic.keys()])
    while difference > 0.001:
        for page_name in out_links_dic.keys():
            new_PR[page_name] = (1-dampping_factor) + dampping_factor * sum([float(old_PR[page]) / len(out_links_dic[page]) for page in in_links[page_name]])
        difference = sum([abs(old_PR[page_name]-new_PR[page_name]) for page_name in out_links_dic.keys()])
        old_PR = new_PR.copy()
    return new_PR

out_links = {"x": ["y", "x", "z", "x", "a"], "a": ["x", "y", "y", "b"], "z": ["x", "a"], "y": ["y", "z", "s", "s"]}
print str(create_in_links(out_links))
