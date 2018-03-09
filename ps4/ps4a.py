# Problem Set 4A
# Name: <Narendra Parigi>
# Collaborators:
# Time Spent: x:xx

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''
    #base case
    out = []
    if len(sequence) == 1:
        return [sequence]
    else:
        #recursion
        for i, let in enumerate(sequence):
            for perm in get_permutations(sequence[:i] + sequence[i+1:]):
                out += [let + perm]
    return out

if __name__ == '__main__':
#    #EXAMPLE
#    example_input = 'abc'
#    print('Input:', example_input)
#    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
#    print('Actual Output:', get_permutations(example_input))
    
#    # Put three example test cases here (for your sanity, limit your inputs
#    to be three characters or fewer as you will have n! permutations for a 
#    sequence of length n)
    example_input = 'abc'
    print('Input:', example_input)
    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
    print('Actual Output:', get_permutations(example_input))
    print('Output Length:', len(get_permutations(example_input)))
    print('Actual Output:', get_permutations('abcd'))
    print('Output Length:', len(get_permutations('abcd')))
    print('Actual Output:', get_permutations('abcde'))
    print('Output Length:', len(get_permutations('abcde')))