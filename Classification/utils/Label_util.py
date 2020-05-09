from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import *

import pandas as pd
from snorkel.models import StableLabel
from snorkel.db_helpers import reload_annotator_labels
from sqlalchemy import Column

# importing modules from a different directory is different between systems and python versions
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '../data_gathering')
try:
    import data_gathering.consts as consts
    print("consts imported")
except:
    try:
        import consts as consts
        print("consts imported")
    except:
        try:
            from .consts import consts as consts
            print("consts imported")
        except:
            try:
                from data_gathering import consts as consts
                print("consts imported")
            except:
                print("couldn't import consts")

FPATH = consts.GOLD_LABELS


def load_external_labels(session, candidate_class, annotator_name='gold'):
    gold_labels = pd.read_csv(FPATH, delimiter='\t',encoding='utf-8')
    for index, row in gold_labels.iterrows():    
        # We check if the label already exists, in case this cell was already executed
        context_stable_ids = "~~".join([row['cell']])
        
        # print(index, context_stable_ids)
        # print(StableLabel.context_stable_ids)
        query = session.query(StableLabel).filter(StableLabel.context_stable_ids == context_stable_ids)
        query = query.filter(StableLabel.annotator_name == annotator_name)

        if query.count() == 0:

            session.add(StableLabel(
                context_stable_ids=context_stable_ids,
                annotator_name=annotator_name,
                value=row['label']))

    print(index)
    # Commit session
    session.commit()

    # Reload annotator labels
    reload_annotator_labels(session, candidate_class, annotator_name, split=1, filter_label_split=False)
    reload_annotator_labels(session, candidate_class, annotator_name, split=2, filter_label_split=False)
