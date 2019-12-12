import argparse

import pandas as pd


def main(args):
    """ Output titles and comments to file for TopMne
    """
    posts = pd.read_csv(args.posts, index_col="id")
    comments = pd.read_csv(args.comments, index_col="id")
    posts.title.to_csv("../data/topmine_posts.txt", header=False, index=None)
    comments.body.to_csv("../data/topmine_comments.txt", header=False, index=None)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Preprocesses dataset")
    parser.add_argument(
        "--posts",
        action="store",
        default="../data/posts.csv",
        help="path to posts csv file",
    )
    parser.add_argument(
        "--comments",
        action="store",
        default="../data/comments.csv",
        help="path to comments csv file",
    )
    main(parser.parse_args())
