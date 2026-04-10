-- Seed inicial de raças populares
INSERT INTO racas (nome, especie, porte, expectativa_vida_anos, descricao, nivel_atividade) VALUES
('Golden Retriever', 'cao', 'grande', 12, 'Cão amigável, inteligente e dedicado. Ótimo para famílias.', 'alto'),
('Labrador Retriever', 'cao', 'grande', 12, 'Um dos cães mais populares do mundo. Dócil e brincalhão.', 'alto'),
('Bulldog Francês', 'cao', 'pequeno', 10, 'Compacto, muscular e afetivo. Adapta-se bem a apartamentos.', 'baixo'),
('Poodle', 'cao', 'medio', 14, 'Altamente inteligente e hipoalergênico. Ótimo para pessoas com alergia.', 'medio'),
('Yorkshire Terrier', 'cao', 'pequeno', 14, 'Pequeno e corajoso. Muito apegado ao dono.', 'medio'),
('Shih Tzu', 'cao', 'pequeno', 13, 'Carinhoso e tranquilo. Ideal para idosos e apartamentos.', 'baixo'),
('Border Collie', 'cao', 'medio', 14, 'O cão mais inteligente do mundo. Precisa de muito estímulo mental.', 'alto'),
('Dachshund', 'cao', 'pequeno', 14, 'Curioso e teimoso. Adora cavar e farejar.', 'medio'),
('Pastor Alemão', 'cao', 'grande', 11, 'Leal, corajoso e versátil. Excelente cão de trabalho.', 'alto'),
('Persa', 'gato', 'medio', 15, 'Tranquilo e elegante. Requer cuidados especiais com o pelo.', 'baixo'),
('Siamês', 'gato', 'medio', 15, 'Vocal e social. Gosta de interação constante.', 'medio'),
('Maine Coon', 'gato', 'grande', 14, 'Um dos maiores gatos domésticos. Gentil e brincalhão.', 'medio'),
('British Shorthair', 'gato', 'medio', 15, 'Calmo e independente. Adapta-se bem a diversas rotinas.', 'baixo'),
('Vira-lata / SRD', 'cao', 'medio', 15, 'Mistura de raças. Geralmente muito saudável e resistente.', 'medio')
ON CONFLICT (nome) DO NOTHING;

-- Cuidados padrão para Golden Retriever (id será 1)
INSERT INTO cuidados (raca_id, categoria, titulo, descricao, frequencia, prioridade)
SELECT id, 'alimentacao', 'Ração Premium para Raças Grandes',
    'Golden Retrievers necessitam de ração específica para raças grandes com controle de cálcio e fósforo para proteger as articulações.',
    'diário', 'alta'
FROM racas WHERE nome = 'Golden Retriever'
ON CONFLICT DO NOTHING;

INSERT INTO cuidados (raca_id, categoria, titulo, descricao, frequencia, prioridade)
SELECT id, 'higiene', 'Escovação do Pelo',
    'O pelo dourado do Golden precisa ser escovado regularmente para evitar nós e remover pelos mortos, especialmente na muda.',
    'semanal', 'alta'
FROM racas WHERE nome = 'Golden Retriever'
ON CONFLICT DO NOTHING;

INSERT INTO cuidados (raca_id, categoria, titulo, descricao, frequencia, prioridade)
SELECT id, 'saude', 'Monitoramento de Displasia Coxofemoral',
    'Golden Retrievers são predispostos a displasia coxofemoral. Manter peso ideal e fazer exames regulares é essencial.',
    'anual', 'alta'
FROM racas WHERE nome = 'Golden Retriever'
ON CONFLICT DO NOTHING;
