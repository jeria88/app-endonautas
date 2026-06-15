def evaluate(test, raw_scores, questions):
    by_dim = {}
    for q in questions:
        key = q.dimension_key or 'total'
        by_dim.setdefault(key, []).append(raw_scores.get(str(q.pk), 0))

    result = {}
    for key, scores in by_dim.items():
        total = sum(scores)
        avg = total / len(scores) if scores else 0
        result[key] = {'total': total, 'avg': round(avg, 2), 'count': len(scores)}

    result['_total'] = sum(raw_scores.values())
    return result
