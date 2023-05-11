import pickle
import pandas as pd
import numpy as np

from .config import MODELS_FOLDER


# Load feature tables
users_data = pd.read_csv(MODELS_FOLDER + 'users_data.csv', index_col=0)
jokes_data = pd.read_csv(MODELS_FOLDER + 'jokes_data.csv', index_col=0)
jokes_data['text'] = jokes_data['text'].astype('string')
# Load models
with open(MODELS_FOLDER + 'svd.pk', 'rb') as f:
    svd = pickle.load(f)
with open(MODELS_FOLDER + 'blender.pk', 'rb') as f:
    blender = pickle.load(f)
with open(MODELS_FOLDER + 'ranker.pk', 'rb') as f:
    ranker = pickle.load(f)
# Load precalculated cold (popularity based) recommendations
with open(MODELS_FOLDER + 'cold_recommendations.pk', 'rb') as f:
    cold_recommendations = pickle.load(f)
# Load dict with jokes that users have already seen
with open(MODELS_FOLDER + 'user_jokes.pk', 'rb') as f:
    user_jokes = pickle.load(f)


def get_recommendations(uid: int) -> list:
    if uid in users_data['uid'].unique():
        return get_warm_recommendations(uid)
    else:
        return cold_recommendations


def get_warm_recommendations(uid: int, k: int = 10) -> list:
    # Generate dataframe for models inference
    user_df = pd.DataFrame({
        'uid': [uid] * 100,
        'jid': range(1, 101),
        'svd': [svd.predict(uid, jid, verbose=False).est for jid in range(1, 101)],
    })
    user_df = user_df.\
        join(jokes_data.add_prefix('joke_'), on='jid').\
        join(users_data.add_prefix('user_'), on='uid').\
        drop(['joke_jid', 'user_uid'], axis=1)

    print(user_df.info())

    # Get ranker scores
    scores = ranker.predict(user_df.drop(['uid', 'jid'], axis=1))
    # Lower scores of jokes, that user have seen
    for jid in user_jokes[uid]:
        scores[jid-1] -= 100
    # Get top K recommendations
    top_recommendations = np.argsort(-scores) + 1
    top_recommendations = top_recommendations[:k].tolist()

    # Get top recommendation rating
    top_recommendation = top_recommendations[0]
    top_recommendation_rating = blender.predict(
        user_df[user_df['jid'] == top_recommendation].drop(['uid', 'jid'], axis=1)
    )[0]

    return [
        {top_recommendation: top_recommendation_rating},
        top_recommendations
    ]
