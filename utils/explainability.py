import numpy as np

def get_top_keywords(model, vectorizer, text, top_n=5):
    vec = vectorizer.transform([text])

    if vec.nnz == 0:
        return ["Insufficient textual information"]

    feature_names = vectorizer.get_feature_names_out()
    class_index = model.predict(vec)[0]
    class_pos = list(model.classes_).index(class_index)

    coefs = model.coef_[class_pos]
    scores = vec.toarray()[0] * coefs

    top_indices = np.argsort(scores)[-top_n:][::-1]
    keywords = [feature_names[i] for i in top_indices if scores[i] > 0]

    return keywords if keywords else ["Low confidence keywords"]
