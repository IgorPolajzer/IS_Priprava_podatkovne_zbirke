#!/bin/bash

PROGRAM=".venv/bin/python"
DATA="data_set"
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

echo "Začenjam celovito testiranje vseh kombinacij..."

for FILE in "$DATA"/*.csv; do
    echo "Datoteka: $FILE"

    # 1. k-NN (12 kombinacij)
    for n in 1 5 21; do
        for w in uniform distance; do
            for m in euclidean manhattan; do
                $PROGRAM main.py -knn $n $w $m $FILE
            done
        done
    done

    # 2. Logistic Regression (12 kombinacij)
    for c in 0.01 1.0 100.0; do
        for p in l2 None; do
            for s in lbfgs saga; do
                $PROGRAM main.py -lr $c $p $s $FILE
            done
        done
    done

    # 3. Decision Tree (18 kombinacij)
    for d in 3 10 None; do
        for c in gini entropy; do
            for l in 1 5 20; do
                $PROGRAM main.py -dtc $d $c $l $FILE
            done
        done
    done

    # 4. Random Forest (8 kombinacij)
    for n in 10 100; do
        for f in sqrt log2; do
            for b in True False; do
                $PROGRAM main.py -rfc $n $f $b $FILE
            done
        done
    done

    # 5. AdaBoost (hp3 je zdaj max_depth osnovnega drevesa: 1 ali 2)
    for n in 50 100; do
        for r in 0.1 1.0; do
            for d in 1 2; do
                $PROGRAM main.py -abc $n $r $d $FILE
            done
        done
    done

    # 6. Gaussian NB (2 kombinaciji)
    for v in 1e-9 1e-5; do
        $PROGRAM main.py -gnb $v 0 0 $FILE
    done

    # 7. Linear SVC (12 kombinacij)
    for c in 0.1 1.0 10.0; do
        for l in hinge squared_hinge; do
            for t in 1e-4 1e-3; do
                $PROGRAM main.py -lsvc $c $l $t $FILE
            done
        done
    done

    # 8. MLP (8 kombinacij)
    for h in "50" "100,50"; do
        for a in relu tanh; do
            for r in 0.0001 0.05; do
                $PROGRAM main.py -mlp "$h" $a $r $FILE
            done
        done
    done

    # 9. SGD (12 kombinacij)
    for l in hinge log_loss; do
        for p in l1 l2 elasticnet; do
            for r in constant adaptive; do
                $PROGRAM main.py -sgd $l $p $r $FILE
            done
        done
    done

    # 10. Extra Trees (8 kombinacij)
    for n in 100 200; do
        for d in 10 20; do
            for s in 2 10; do
                $PROGRAM main.py -etc $n $d $s $FILE
            done
        done
    done

done

echo "Testiranje končano. Rezultati so v results.txt."