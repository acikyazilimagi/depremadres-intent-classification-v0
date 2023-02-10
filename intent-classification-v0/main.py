import rule_based_clustering as rbc
#import pg_ops
import run_zsc as zsc
from tqdm import tqdm
import pandas as pd



#conn = pg_ops.connect_to_db()

plot_data = {"key": rbc.labels, "count": [0] * len(rbc.labels)}

# is_done -> False/True based on processed or not
# intent_result -> labels with separated by comma
# Get data
#data = pg_ops.get_data(conn, 'tweets_depremaddress', ['id', 'full_text'], 'is_done = False OR is_done = True') # intent_result
data = pd.read_csv("intent-classification-v0\sample_data.csv")
# mock call for getting multiple clause filtered data
# data = pg_ops.get_data(conn, 'tweets_depremaddress', ['id', 'full_text'], 'is_done = True AND (intent_result = '') IS NOT FALSE')
# print("Data: {}".format(data))
print("Data length: {}".format(len(data)))

# for row in tqdm(data):
for row in data:
    rule_based_labels, plot_data = rbc.process_tweet(row, plot_data)
    intent_results = ",".join(rule_based_labels) if rule_based_labels else ""

    if intent_results == "":

        zsc_result = zsc.query(
            {
                "inputs": row[1],
                "parameters": {"candidate_labels": rbc.labels},
            })

        if zsc_result is not None:
            # sequence, labels, scores
            if "scores" in zsc_result:
                label_scores = zsc_result["scores"]
                labels_filtered = [zsc_result["labels"][i] for i in range(len(label_scores)) if label_scores[i] > 0.3]
                intent_results = ",".join([label for label in labels_filtered])                
                plot_data = rbc.update_plot_data(plot_data, labels_filtered)
    # query = "UPDATE tweets_depremaddress SET intent=%s, is_done=True WHERE id=%s", (intent_results, row[0])
    # print(query)
    # cur = conn.cursor()
    # cur.execute("UPDATE tweets_depremaddress SET intent_result=%s, is_done=True WHERE id=%s", (intent_results, row[0]))
    # conn.commit()

rbc.draw_plot(plot_data)
# conn.close()