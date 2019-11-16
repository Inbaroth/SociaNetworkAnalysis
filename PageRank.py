import pandas as pd


out_edges_dict = {}
in_edges_dict = {}
pages_rank_dict = {}
calculate_pagerank_activated = False


def load_graph(path):
    try:
        df = pd.read_csv(path, header=None)
    except FileNotFoundError:
        print("an error occurred while trying to read the file")
        exit(1)

    for row in df.iterrows():
        source = str(row[1][0])
        dest = str(row[1][1])

        # initialize the out_edges and in_edges dicts:
        if not out_edges_dict.get(source):
            out_edges_dict[source] = [dest]
        else:
            out_edges_dict[source].append(dest)

        if not in_edges_dict.get(dest):
            in_edges_dict[dest] = [source]
        else:
            in_edges_dict[dest].append(source)

        # initialize pages_rank_dict:
        if not pages_rank_dict.get(source):
            pages_rank_dict[source] = 0
        if not pages_rank_dict.get(dest):
            pages_rank_dict[dest] = 0


def calculate_page_rank(beta, delta, max_iterations):
    next_pages_rank_dict = {}
    sum_diff_smaller_then_delta = False
    sum = 0
    # iteration 0
    for page in pages_rank_dict:
        pages_rank_dict[page] = 1/len(pages_rank_dict)
    while max_iterations > 0 and not sum_diff_smaller_then_delta:
        sum_diff = 0
        for page in pages_rank_dict:
            sum_indeg = 0
            if page not in in_edges_dict:
                pages_rank_dict[page] = 0
            if page in in_edges_dict:
                for in_deg in in_edges_dict[page]:
                    sum_indeg = sum_indeg + beta * (pages_rank_dict[in_deg] / len(out_edges_dict[in_deg]))
                next_pages_rank_dict[page] = sum_indeg
                sum = sum + sum_indeg
        max_iterations = max_iterations - 1
        for i in next_pages_rank_dict:
            prev_pagerank = pages_rank_dict[i]
            pages_rank_dict[i] = next_pages_rank_dict[i] + (1-sum) / len(pages_rank_dict)
            sum_diff = sum_diff + abs(pages_rank_dict[i]-prev_pagerank)
        if sum_diff < delta:
            sum_diff_smaller_then_delta = True
        next_pages_rank_dict = {}
        sum = 0
    global calculate_pagerank_activated
    calculate_pagerank_activated = True


def get_PageRank(node_name):
    if not calculate_pagerank_activated:
        return -1
    if node_name not in pages_rank_dict:
        return -1
    else:
        return pages_rank_dict[node_name]


def get_top_nodes(n):
    highest_pagerank_n_pages = list()
    sorted_pagerank_dict = get_all_PageRank()
    if 0 < n < len(pages_rank_dict):
        i = 0
        while i < n:
            highest_pagerank_n_pages.append(sorted_pagerank_dict[i])
            i = i + 1
        return highest_pagerank_n_pages
    if n > len(pages_rank_dict):
        return get_all_PageRank()


def get_all_PageRank():
    all_page_rank = list()
    if not calculate_pagerank_activated:
        return all_page_rank
    sorted_pagerank_dict = sorted(pages_rank_dict.items(), key=lambda x: x[1], reverse=True)
    return sorted_pagerank_dict


def main():
    load_graph("C:\\Users\\amiri\\Desktop\\Wikipedia_votes.csv")
    print("out_edges_dict")
    print(out_edges_dict)
    print("in_edges_dict")
    print(in_edges_dict)
    print("pages_rank_dict")
    calculate_page_rank(1, 0.001, 20)
    print(pages_rank_dict)
    print("get_PageRank: 3")
    print(get_PageRank("3"))
    print("get_top_nodes: 2")
    print(get_top_nodes(2))
    print("get_all_PageRank")
    print(get_all_PageRank())


if __name__ == '__main__':
    main()
