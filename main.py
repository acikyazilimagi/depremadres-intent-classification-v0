import rule_based_clustering as rbc
import pg_ops

conn = pg_ops.connect_to_db()

# is_done -> False/True based on processed or not
# intent_result -> labels with separated by comma
# Get data
data = pg_ops.get_data(conn, 'tweets_depremaddress', ['id', 'full_text'], 'is_done = False')

for row in data:
    processed_text = rbc.process_tweet(row)
    intent_results = ""
    if processed_text is not None:
        intent_results = ",".join(processed_text)
    query = "UPDATE tweets_depremaddress SET intent=%s, is_done=True WHERE id=%s", (intent_results, row[0])
    print(query)
    cur = conn.cursor()
    cur.execute("UPDATE tweets_depremaddress SET intent_result=%s, is_done=True WHERE id=%s", (intent_results, row[0]))
    conn.commit()

conn.close()