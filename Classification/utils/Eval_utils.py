from snorkel.annotations import load_gold_labels
from snorkel.models import Context, Document, Sentence, Span, Candidate
import numpy as np

def binary_scores_from_counts(ntp, nfp, ntn, nfn):
    """
    Precision, recall, and F1 scores from counts of TP, FP, TN, FN.
    Example usage:
        p, r, f1 = binary_scores_from_counts(*map(len, error_sets))
    """
    prec = ntp / float(ntp + nfp) if ntp + nfp > 0 else 0.0
    rec = ntp / float(ntp + nfn) if ntp + nfn > 0 else 0.0
    f1 = (2 * prec * rec) / (prec + rec) if prec + rec > 0 else 0.0
    return prec, rec, f1


def print_scores(ntp, nfp, ntn, nfn, title='Scores'):
    prec, rec, f1 = binary_scores_from_counts(ntp, nfp, ntn, nfn)
    pos_acc = ntp / float(ntp + nfn) if ntp + nfn > 0 else 0.0
    neg_acc = ntn / float(ntn + nfp) if ntn + nfp > 0 else 0.0
    print("========================================")
    print(title)
    print("========================================")
    print("Pos. class accuracy: {:.3}".format(pos_acc))
    print("Neg. class accuracy: {:.3}".format(neg_acc))
    print("Precision            {:.3}".format(prec))
    print("Recall               {:.3}".format(rec))
    print("F1                   {:.3}".format(f1))
    print("----------------------------------------")
    print("TP: {} | FP: {} | TN: {} | FN: {}".format(ntp, nfp, ntn, nfn))
    print("========================================\n")


def run_lf_arr_as_one(lf_arr, c):
    str_to_int = ['NA', 'Load Data', 'Prep & Clean', 'Train & Param', 'Eval', 'Explore', 'Import']
    for func in lf_arr:
        res = func(c)
        if res != None:
            return str_to_int.index(res)
    return 0


def test_LF(session, lf_arr, label_val, split=1, annotator_name='gold'):

    test_candidates = session.query(Candidate).filter(Candidate.split == split).all()
    test_labels = load_gold_labels(session, annotator_name='gold', split=split)
    test_marginals = np.array([(run_lf_arr_as_one(lf_arr, c)) for c in test_candidates])

    test_label_array = []
    tp = set()
    fp = set()
    tn = set()
    fn = set()
    b = 0.5

    for i, candidate in enumerate(test_candidates):
        try:
            test_label_index = test_labels.get_row_index(candidate)
            test_label = test_labels[test_label_index, 0]
        except AttributeError:
            test_label = test_labels[i]

        # Bucket the candidates for error analysis
        test_label_array.append(test_label)
        if test_label != 0:
            if test_marginals[i] > b:
                if test_label == label_val:
                    tp.add(candidate)
                else:
                    fp.add(candidate)
            elif test_marginals[i] < b:
                if test_label != label_val:
                    tn.add(candidate)
                else:
                    fn.add(candidate)

    print_scores(len(tp), len(fp), len(tn), len(fn), title="Scores (Un-adjusted)")
    return tp, fp, tn, fn


def calc_lf_acc(session, tag_cand_index, L_test, test_marginals, df, show_errs=False):
    # Calculates accuracy of labeled cells in dev set
    dev_c = 0
    dev_ic = 0

    y_pred = []
    y_true = []

    for i in tag_cand_index:
        cand = L_test.get_candidate(session, i)
        cell_id = cand.cell.stable_id
        cell_txt = cand.cell.text
        cell_LF = cand.labels
        cell_pred = np.where(test_marginals[i] == max(test_marginals[i]))[0][0] + 1
        is_tagged = len(df[df["cell"] == cell_id])
        if is_tagged > 0:
            cell_label = df[df["cell"] == cell_id].iloc[0, 1]
            y_true.append(float(cell_label))
            y_pred.append(float(cell_pred))
            if cell_label == cell_pred:
                dev_c += 1
            else:
                dev_ic += 1
                if show_errs:
                    print("cell_id", cell_id)
                    print("cell_txt", cell_txt)
                    print("cell_pred:", cell_pred, "  |   cell_label:", cell_label)
                    print("cell_LF", cell_LF)
                    print("----------------\n")

    print("Accuracy - ", str((dev_c / float(dev_c + dev_ic)) * 100) + "%")

    return y_pred, y_true

