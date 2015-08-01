"""
    Computing alignment of sequences
    """

# general import


# Matrix functions
def build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score):
    """
    return a dictionary of dictionaries whose entries are indexed by pairs of characters in alphabet plus '-'.
    """
    scoring_matrix = {}
    for row_char in alphabet:
        temp_score = {}  # store temperory dictionaries
        for col_char in alphabet:
            if row_char == col_char:
                temp_score[col_char] = diag_score
            else:
                temp_score[col_char] = off_diag_score
        temp_score['-'] = dash_score
        scoring_matrix[row_char] = temp_score.copy()

    temp_score = {}  # store temperory dictionaries
    for col_char in alphabet:
        temp_score[col_char] = dash_score
    temp_score['-'] = dash_score
    scoring_matrix['-'] = temp_score.copy()

    return scoring_matrix

def compute_alignment_matrix(seq_x, seq_y, scoring_matrix, global_flag):
    """
    return the alignment matrix for seq_x and seq_y.
    """
    score = []
    # initialization
    for dummy_i in range(len(seq_x)+1):
        score_temp = [0 for dummy_j in range(len(seq_y)+1)]
        score.append(score_temp[:])
    
    score[0][0] = 0
    if global_flag:
        for dummy_i in range(1, len(seq_x)+1):
            score[dummy_i][0] = score[dummy_i-1][0] + scoring_matrix[seq_x[dummy_i-1]]['-']
        
        for dummy_j in range(1, len(seq_y)+1):
            score[0][dummy_j] = score[0][dummy_j-1] + scoring_matrix['-'][seq_y[dummy_j-1]]
        for dummy_i in range(1, len(seq_x)+1):
            for dummy_j in range(1, len(seq_y)+1):
                score[dummy_i][dummy_j] = max(score[dummy_i-1][dummy_j-1] + scoring_matrix[seq_x[dummy_i-1]][seq_y[dummy_j-1]],
                                    score[dummy_i-1][dummy_j] + scoring_matrix[seq_x[dummy_i-1]]['-'],
                                    score[dummy_i][dummy_j-1] + scoring_matrix['-'][seq_y[dummy_j-1]] )
    else:
        for dummy_i in range(1, len(seq_x)+1):
            score[dummy_i][0] = 0
        for dummy_j in range(1, len(seq_y)+1):
            score[0][dummy_j] = 0
        for dummy_i in range(1, len(seq_x)+1):
            for dummy_j in range(1, len(seq_y)+1):
                score[dummy_i][dummy_j] = max(score[dummy_i-1][dummy_j-1] + scoring_matrix[seq_x[dummy_i-1]][seq_y[dummy_j-1]],
                                    score[dummy_i-1][dummy_j] + scoring_matrix[seq_x[dummy_i-1]]['-'],
                                    score[dummy_i][dummy_j-1] + scoring_matrix['-'][seq_y[dummy_j-1]] )
                if score[dummy_i][dummy_j] < 0:
                    score[dummy_i][dummy_j] = 0
    return score

# Alignment function
def compute_global_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    """
    computes a global alignment of seq_x and seq_y using the global alignment matrix alignment_matrix.
    returns a tuple of the form (score, align_x, align_y),
    where score is the score of the global alignment align_x and align_y.
    """
    dummy_i = len(seq_x)
    dummy_j = len(seq_y)
    align_x = ''
    align_y = ''
    while (dummy_i != 0 and dummy_j != 0):
        if alignment_matrix [dummy_i][dummy_j] == alignment_matrix[dummy_i-1][dummy_j-1] + scoring_matrix[seq_x[dummy_i-1]][seq_y[dummy_j-1]]:
            align_x = seq_x[dummy_i-1] + align_x
            align_y = seq_y[dummy_j-1] + align_y
            dummy_i -= 1
            dummy_j-=1
        else:
            if alignment_matrix[dummy_i][dummy_j] == alignment_matrix[dummy_i-1][dummy_j] + scoring_matrix[seq_x[dummy_i-1]]['-']:
                align_x = seq_x[dummy_i-1] + align_x
                align_y = '-' + align_y
                dummy_i -= 1
            else:
                align_y = seq_y[dummy_j-1] + align_y
                align_x = '-' + align_x
                dummy_j -= 1
    while dummy_i != 0:
        align_x = seq_x[dummy_i-1] + align_x
        align_y = '-' + align_y
        dummy_i -= 1
    while dummy_j != 0:
        align_x = '-' + align_x
        align_y = seq_y[dummy_j-1] + align_y
        dummy_j -= 1

    return alignment_matrix[len(seq_x)][len(seq_y)], align_x, align_y

def compute_local_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    """
    computes a local alignment of seq_x and seq_y using the local alignment matrix alignment_matrix.
    returns a tuple of the form (score, align_x, align_y), where score is the score
    of the optimal local alignment align_x and align_y.
    """
    dummy_i = len(seq_x)
    dummy_j = len(seq_y)
    align_x = ''
    align_y = ''
        
    #find the maximum value over the entire matrix
    max_score = 0
    for dummy_idx1 in range(len(seq_x)+1):
        for dummy_idx2 in range(len(seq_y)+1):
            if alignment_matrix[dummy_idx1][dummy_idx2] > max_score:
                dummy_i = dummy_idx1
                dummy_j = dummy_idx2
                max_score = alignment_matrix[dummy_idx1][dummy_idx2]

    # trace back
    while (dummy_i != 0 and dummy_j != 0 and alignment_matrix [dummy_i][dummy_j] != 0):
        if alignment_matrix [dummy_i][dummy_j] == alignment_matrix[dummy_i-1][dummy_j-1] + scoring_matrix[seq_x[dummy_i-1]][seq_y[dummy_j-1]]:
            align_x = seq_x[dummy_i-1] + align_x
            align_y = seq_y[dummy_j-1] + align_y
            dummy_i -= 1
            dummy_j-=1
        else:
            if alignment_matrix[dummy_i][dummy_j] == alignment_matrix[dummy_i-1][dummy_j] + scoring_matrix[seq_x[dummy_i-1]]['-']:
                align_x = seq_x[dummy_i-1] + align_x
                align_y = '-' + align_y
                dummy_i -= 1
            else:
                align_y = seq_y[dummy_j-1] + align_y
                align_x = '-' + align_x
                dummy_j -= 1


    return max_score, alignment_matrix[len(seq_x)][len(seq_y)], align_x, align_y

if __name__ == "__main__":
    dict = build_scoring_matrix(set(['A', 'C', 'T', 'G']), 6, 2, -4)
    print dict
    scoreT = compute_alignment_matrix('AA','TAAT', dict, True)
    score = compute_alignment_matrix('AA','TAAT', dict, False)
    print score
    seq_x = 'AA'
    seq_y = 'TAAT'
    print compute_global_alignment(seq_x, seq_y, dict, scoreT)
    print compute_local_alignment(seq_x, seq_y, dict, score)