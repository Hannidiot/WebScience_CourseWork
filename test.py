from NewsWorthinessMarker import TweetNewsWorthinessMarker


if __name__ == '__main__':
    import json

    with open('/Users/minhao/Workspace/WS-Proj/CourseWork-M/data/highFileFeb', 'r') as f:
        high_value_set = []
        for line in f.readlines():
            high_value_set.append(json.loads(line))

    with open('/Users/minhao/Workspace/WS-Proj/CourseWork-M/data/lowFileFeb', 'r') as f:
        low_value_set = []
        for line in f.readlines():
            low_value_set.append(json.loads(line))
    
    t = TweetNewsWorthinessMarker(high_value_set, low_value_set)    
    
    samples = []
    with open('data/geoLondonJan', 'r') as f:
        for line in f.readlines():
            samples.append(json.loads(line))

    f = open('tmp3.txt', 'w')

    cnt = 0
    for sample in samples:
        text = sample['text']
        if t.is_high_quality(text):
            cnt += 1
            f.write(f'{t.mark(text)}:{text}\n\n')
    
    print(cnt)
    f.close()
