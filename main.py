import rule_based_clustering as rbc
import pg_ops
import run_zsc as zsc

labels = ["KURTARMA", "YEMEK-SU", "GIYSI"]
conn = pg_ops.connect_to_db()

plot_data = {"key": labels, "count": [0 for i in range(len(labels))]}

# is_done -> False/True based on processed or not
# intent_result -> labels with separated by comma
# Get data
data = pg_ops.get_data(conn, 'tweets_depremaddress', ['id', 'full_text'], 'is_done = False')
for row in data:
    rule_based_labels, plot_data = rbc.process_tweet(row, plot_data)
    intent_results = ""
    if rule_based_labels is not None:
        intent_results = ",".join(rule_based_labels)
    elif intent_results == "":
        zsc_result = zsc.query(
                {
                    "inputs": row[1],
                    "parameters": {"candidate_labels": labels},
                })
        if zsc_result is not None:
            # sequence, labels, scores
            if "scores" in zsc_result:
                label_scores = zsc_result["scores"]
                intent_results = ",".join([zsc_result["labels"][i] for i in range(len(label_scores)) if label_scores[i] > 0.3])
    query = "UPDATE tweets_depremaddress SET intent=%s, is_done=True WHERE id=%s", (intent_results, row[0])
    print(query)
    cur = conn.cursor()
    cur.execute("UPDATE tweets_depremaddress SET intent_result=%s, is_done=True WHERE id=%s", (intent_results, row[0]))
    conn.commit()

# rbc.draw_plot(plot_data)
conn.close()