import rule_based_clustering as rbc
import pg_ops
import run_zsc as zsc

labels = ["KURTARMA", "YEMEK-SU", "GIYSI"]
conn = pg_ops.connect_to_db()

# is_done -> False/True based on processed or not
# intent_result -> labels with separated by comma
# Get data
data = pg_ops.get_data(conn, 'tweets_depremaddress', ['id', 'full_text'], 'is_done = False')
print("data: ", data)
for row in data:
    rule_based_labels = rbc.process_tweet(row)
    intent_results = ""
    print("=====================================")
    if rule_based_labels is not None:
        intent_results = ",".join(rule_based_labels)
        print("intent results from rule-based: ", intent_results)
    elif intent_results == "":
        zsc_result = zsc.query(
                {
                    "inputs": row[1],
                    "parameters": {"candidate_labels": labels},
                })
        print("zsc result: ", zsc_result)
        label_scores = zsc_result["scores"]
        intent_results = ",".join([zsc_result["labels"][i] for i in range(len(label_scores)) if label_scores[i] > 0.3])
    print("intent results from zsc: ", intent_results)
    print("=====================================")
    # query = "UPDATE tweets_depremaddress SET intent=%s, is_done=True WHERE id=%s", (intent_results, row[0])
    # print(query)
    # cur = conn.cursor()
    # cur.execute("UPDATE tweets_depremaddress SET intent_result=%s, is_done=True WHERE id=%s", (intent_results, row[0]))
    # conn.commit()

conn.close()