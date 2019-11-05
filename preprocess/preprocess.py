import argparse
import pickle as pkl
import re

import pandas as pd
from pandas.io.json import json_normalize


def clean_title(x):
    tag = r"\b((\d{1,2})[\s\(\)\[\],\/-]*([mf]|female|male))\b|\b(([mf]|female|male)[\s\(\)\[\],\/-]*(\d{1,2}))\b"
    age = r"\d{1,2}"
    gender = r"(\b|\d)([mMfF])"
    match = re.search(tag, x, flags=re.I)
    if match:
        matched = match.group(0)
        extracted_age = int(re.search(age, matched).group(0))
        extracted_gender = re.search(gender, matched).group(2).upper()
        if extracted_age < 18 or extracted_age > 50:
            return None, None
        return extracted_age, extracted_gender
    return None, None


def extract_rating(comment):
    rating_re = r"\b(\d{1}(\.\d+)?(['\"])?)(\/\d+)?(ish)?\b"
    height_re = r"\d+('|\")"
    match = re.search(rating_re, comment)
    if match:
        rating = match.group(1)
        # this conditional just makes sure this isn't a false positive that catches the height
        if re.search(height_re, rating) is None:
            return float(rating)
    return None


def main(args):
    """ Run preprocessing on data
        Extract age / gender from posts
        Extract rating from comments
    """
    print("Reading pickle dumps:")
    print("Opening and json normalizing {}".format(args.posts))
    posts = pkl.load(open(args.posts, "rb"))
    posts_df = json_normalize(posts)
    print("Opening and json normalizing {}".format(args.comments))
    comments = pkl.load(open(args.comments, "rb"))
    comments_df = json_normalize(comments)

    print("Preprocessing Posts")
    posts_df = posts_df[
        [
            "author",
            "full_link",
            "id",
            "num_comments",
            "title",
            "gilded",
            "score",
            "selftext",
            "total_awards_received",
        ]
    ]
    posts_df = posts_df.set_index("id")
    age_gender = posts_df["title"].apply(clean_title)
    posts_df["age"] = age_gender.apply(lambda x: x[0] if x is not None else None)
    posts_df["gender"] = age_gender.apply(lambda x: x[1] if x is not None else None)

    print("Preprocessing Comments")
    comments_df = comments_df[
        [
            "gilded",
            "author",
            "body",
            "is_submitter",
            "score",
            "controversiality",
            "parent_id",
            "link_id",
            "id",
        ]
    ]
    comments_df = comments_df[comments_df.author != "AutoModerator"]
    comments_df["clean_link_id"] = comments_df["link_id"].apply(lambda x: x[3:])
    comments_df["rating"] = comments_df["body"].apply(extract_rating)

    posts_df["average_rating"] = comments_df.groupby("clean_link_id").rating.agg("mean")
    print("Writing outputs to:\n\t{}\n\t{}".format(args.posts_outfile, args.comments_outfile))
    posts_df.to_csv(args.posts_outfile)
    comments_df.to_csv(args.comments_outfile)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Preprocesses dataset")
    parser.add_argument(
        "--posts",
        action="store",
        default="../data/posts_since_2018.pkl",
        help="path to posts dictionary pickle file",
    )
    parser.add_argument(
        "--comments",
        action="store",
        default="../data/comments_since_2018.pkl",
        help="path to comments dictionary pickle file",
    )
    parser.add_argument(
        "--posts_outfile",
        action="store",
        default="../data/posts.csv",
        help="output path of posts csv",
    )
    parser.add_argument(
        "--comments_outfile",
        action="store",
        default="../data/comments.csv",
        help="output path of comments csv",
    )
    args = parser.parse_args()
    main(args)
