import unittest

import parser
import analyzer

class TwitterTestSuite(unittest.TestCase):

    def test_should_remove_whitespaces_corretly(self):
        self.assertEqual("Hello three whitespaces ", parser._fix_whitespaces_excess("Hello   three whitespaces   ")) 
        self.assertEqual("This quote shoulnt change.", parser._fix_whitespaces_excess("This quote shoulnt change."))

    def test_should_remove_retweet_twitter_user_corretly(self):
        self.assertEqual('" ""Em prol da atividade econômica de BH.”', parser._remove_retweet_twitter_username('"RT @JornalDaCidadeO: ""Em prol da atividade econômica de BH.”'))
        self.assertEqual('Sério. https://t.co/2zZaCzbnIe', parser._remove_retweet_twitter_username('RT @JEONS4TAN: Sério. https://t.co/2zZaCzbnIe'))
    
    def test_should_remove_twitter_usernames_correctly(self):
        self.assertEqual('valeu', parser._remove_twitter_usernames('@Adorelou_A valeu'))
        self.assertEqual('mds ficou muito lindo eu amei', parser._remove_twitter_usernames('@KNJG0THIC @kookliart mds ficou muito lindo eu amei'))

    def test_should_remove_emojis_correctly(self):
        self.assertEqual('jacarézinho folhinha', parser._remove_emojis('jacarézinho folhinha 🐊🍁'))
        self.assertEqual('Seu sucesso é o meu também! Vou estar torcendo muito por aqui', parser._remove_emojis('Seu sucesso é o meu também! Vou estar torcendo muito por aqui 🥺'))

    def test_should_remove_hastags_correctly(self):
        self.assertEqual('pequeno texto', parser._remove_hastags('#gostomuitodeescrever #escreverédez #_fãs_de_escrita pequeno texto'))
    
    def test_should_remove_http_links_correctly(self):
        self.assertEqual('gosto de postar muitas noticias, veja os links', parser._remove_http_links('https://t.co/DawzjMxp7W gosto de postar muitas noticias, veja os links https://t.co/DawzjMxp7W'))
    
    def test_should_remove_quotes_excess(self):
        self.assertEqual('"Ronan"', parser._remove_quotes_excess('"""Ronan"'))
    
    def test_should_treat_tweet(self):
        tweet = """Hackers continuam atacando os clubes de #futebol

                    https://t.co/DawzjMxp7W
                    https://t.co/DawzjMxp7W
                    https://t.co/DawzjMxp7W
                    @Adorelou_A @Adorelou_A @Adorelou_A
                    #protecaodedados #cybersecurity #esporte"""
        
        self.assertEqual("Hackers continuam atacando os clubes de", parser.parse_tweet(tweet))
    
    def test_should_predict_phrases_correctly(self):
        self.assertEqual('Positivo', analyzer.classify_tweet('O prefeito de São Paulo está fazendo um ótimo trabalho'))


if __name__ == '__main__':
    unittest.main()