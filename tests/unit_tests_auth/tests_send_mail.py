"""
This module contains the unit tests related to the 'reset password' feature.
"""

from django.core import mail
from django.test import TestCase

from pur_beurre.settings import ALLOWED_HOSTS


class EmailTest(TestCase):
    def test_send_email(self):
        user_mail = 'mon.adresse@mail.com'
                
        # Define message.
        message = f"""
            Bonjour,

            Vous recevez ce courriel parce que vous avez demandé la réinitialisation du mot de passe de votre compte sur {ALLOWED_HOSTS[0]}.

            Merci d'aller sur la page suivante pour choisir un nouveau mot de passe :
            http://lien-vers-la-page-de-reinitialisation-du-mot-de-passe.com
            Pour mémoire, votre identifiant est votre courriel : {user_mail}

            Merci d'utiliser notre site !

            L'équipe Pur Beurre
        """
        
        # Send message.
        mail.send_mail(
            f'Password reset on {ALLOWED_HOSTS[0]}',
            message,
            'pur.beurre.etienne86@gmail.com',
            [user_mail],
            fail_silently=False,
        )

        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)

        # Verify that the subject of the first message is correct.
        self.assertEqual(
            mail.outbox[0].subject,
            f'Password reset on {ALLOWED_HOSTS[0]}'
        )
