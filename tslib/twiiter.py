import requests
from tslib.utils import headers,url
import json
from globals import db
import time
import re

def remove_links(content):
    return re.sub(r'https?://\S+|www\.\S+', '', content)


def main(post_link):
    post_id = post_link.split('/')[-1]
    print(post_id)

    params = (
        ('variables', json.dumps({
            "focalTweetId": post_id,
            "with_rux_injections": False,
            "rankingMode": "Relevance",
            "includePromotedContent": True,
            "withCommunity": True,
            "withQuickPromoteEligibilityTweetFields": True,
            "withBirdwatchNotes": True,
            "withVoice": True
        })),
        ('features', json.dumps({
            "profile_label_improvements_pcf_label_in_post_enabled": True,
            "rweb_tipjar_consumption_enabled": True,
            "responsive_web_graphql_exclude_directive_enabled": True,
            "verified_phone_label_enabled": True,
            "creator_subscriptions_tweet_preview_api_enabled": True,
            "responsive_web_graphql_timeline_navigation_enabled": True,
            "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
            "premium_content_api_read_enabled": False,
            "communities_web_enable_tweet_community_results_fetch": True,
            "c9s_tweet_anatomy_moderator_badge_enabled": True,
            "responsive_web_grok_analyze_button_fetch_trends_enabled": False,
            "responsive_web_grok_analyze_post_followups_enabled": True,
            "responsive_web_jetfuel_frame": False,
            "responsive_web_grok_share_attachment_enabled": True,
            "articles_preview_enabled": True,
            "responsive_web_edit_tweet_api_enabled": True,
            "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
            "view_counts_everywhere_api_enabled": True,
            "longform_notetweets_consumption_enabled": True,
            "responsive_web_twitter_article_tweet_consumption_enabled": True,
            "tweet_awards_web_tipping_enabled": False,
            "responsive_web_grok_analysis_button_from_backend": True,
            "creator_subscriptions_quote_tweet_preview_enabled": False,
            "freedom_of_speech_not_reach_fetch_enabled": True,
            "standardized_nudges_misinfo": True,
            "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
            "rweb_video_timestamps_enabled": True,
            "longform_notetweets_rich_text_read_enabled": True,
            "longform_notetweets_inline_media_enabled": True,
            "responsive_web_grok_image_annotation_enabled": True,
            "responsive_web_enhance_cards_enabled": False
        })),
        ('fieldToggles', json.dumps({
            "withArticleRichContentState": True,
            "withArticlePlainText": False,
            "withGrokAnalyze": False,
            "withDisallowedReplyControls": False
        }))
    )

    attempt = 0
    max_retries = 2

    while attempt <= max_retries:
        try:
            start_time = time.time()
            response = requests.get(url=url, headers=headers, params=params, timeout=20)
            data = response.json()
            break
        except requests.exceptions.Timeout:
            attempt += 1
            if attempt > max_retries:
                print(f"Request timed out after {max_retries} retries.")
                return "Failed to fetch post"
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return "Failed to fetch post"

    duration = time.time() - start_time
    print(f"Request completed in {duration:.2f} seconds")

    tweet = data['data']['threaded_conversation_with_injections_v2']['instructions'][0]['entries'][0]['content']['itemContent']['tweet_results']['result']['legacy']
    
    media_url = tweet.get('entities', {}).get('urls', [])
    media_url = [i.get('expanded_url') for i in media_url]
    
    media = tweet.get('extended_entities', {}).get('media', [{}])
    content_type = media[0].get('type', '') if not media_url else 'url'
    img = [i.get('media_url_https') for i in media if i.get('media_url_https')]
    video = [i.get('video_info') for i in media if i.get('video_info')]

    content = remove_links(tweet.get('full_text', ''))
    hashtags = tweet.get('entities', {}).get('hashtags', [])
    if hashtags:
        hashtags = [i.get('text') for i in hashtags]

    print(img, content, hashtags, video)
    db.posts.update_one({'post_id': post_id}, {'$set': {'post_link': post_link, 'content': content, 'content_type': content_type, 'hashtags': hashtags, 'media': {'img': img, 'video': video, 'media_urls': media_url}}}, upsert=True)

    return "post saved"
