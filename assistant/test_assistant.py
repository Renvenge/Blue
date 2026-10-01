"""Testes sem interface gráfica ou coleta real de atividade."""
import unittest
from unittest.mock import patch
import blue_assistant as blue


class Tests(unittest.TestCase):
    def test_cpu_excludes_guest_double_count(self):
        self.assertEqual(blue.cpu_counters('cpu 10 0 10 70 10 0 0 0 5 0\n'), (100, 80))

    def test_memory_uses_available_including_cache(self):
        self.assertEqual(blue.memory_percent('MemTotal: 1000 kB\nMemAvailable: 400 kB\n'), 60)

    def test_no_display_does_not_read_activity(self):
        with patch.dict(blue.os.environ, {}, clear=True), patch.object(blue.subprocess, 'run') as run:
            self.assertEqual(blue.active_app(), 'indisponível')
            run.assert_not_called()

    def test_redirect_is_blocked(self):
        with self.assertRaises(ValueError):
            blue.NoRedirect().redirect_request(None, None, 302, '', {}, 'https://example.com')

    def test_chat_context_and_local_transport(self):
        from unittest.mock import MagicMock
        opener = MagicMock()
        opener.open.return_value.__enter__.return_value.read.return_value = (
            b'{"choices":[{"message":{"content":"Resposta"}}]}')
        with patch.object(blue.urllib.request, 'build_opener', return_value=opener):
            self.assertEqual(blue.ask_local('Ajude', {'cpu_percent': 40}), 'Resposta')
        request = opener.open.call_args.args[0]
        self.assertEqual(request.full_url, 'http://127.0.0.1:8080/v1/chat/completions')
        self.assertIn('40', request.data.decode())


if __name__ == '__main__':
    unittest.main()
