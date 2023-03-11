import arxivscraper
import pickle
import argparse
import os

CATEGORY='cs'
SUB_CAT_LIST=['cs.lg','cs.ai','cs.cv']

def get_arxiv(start_date, end_date):
    print('start scrape from arxiv...')
    scraper = arxivscraper.Scraper(category=CATEGORY, date_from=start_date,date_until=end_date, filters={'categories':SUB_CAT_LIST})
    output = scraper.scrape()
    print('total article scraped:', len(output))
    return output


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--start', type=str, default="2023-03-09")
    parser.add_argument('--end', type=str, default="2023-03-10")
    parser.add_argument('--save_path', type=str, default="./arxiv_data")
    args = parser.parse_args()

    if not os.path.exists(args.save_path):
        os.mkdir(args.save_path)

    results=get_arxiv(args.start, args.end)
    save_file=args.save_path+'/'+args.start+'_'+args.end

    with open(save_file, "wb") as fp:
        pickle.dump(results, fp)

    

