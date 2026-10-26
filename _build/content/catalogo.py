# -*- coding: utf-8 -*-
"""Catálogo de itens por linha de serviço (sem preços).

Fonte dos nomes e das observações técnicas: Tabela 2026 oficial do laboratório,
arquivada em _build/arquivo/ (não publicada). O site não mostra valores: todos os
serviços são informados sob orçamento, pelo WhatsApp ou telefone.
"""

CATS = [
 dict(id='porcelana', title='Porcelana pura (E-Max e zircônia)', items=[
  'Faceta ou coroa em E-Max (pronta)',
  'Restaurado em E-Max (pronto)',
  'Faceta ou coroa em zircônia (pronta)',
  'Restaurado em zircônia (pronto)',
  'Ponte fixa em zircônia (pronta)'],
  obs=['Entregues prontas: coping, aplicação de porcelana e glaze.']),
 dict(id='metaloceramica', title='Metalocerâmica', items=[
  'Coroa metalocerâmica unitária (pronta)',
  'Ponte metalocerâmica (pronta)'],
  obs=['Entregues prontas: coping, aplicação de porcelana e glaze.', 'O metal é orçado à parte.']),
 dict(id='rmf', title='RMF e similares', items=[
  'Restaurado metálico (pronto)',
  'Coroa total metálica (pronta)',
  'Coroa veneer com face em acrílico',
  'Núcleo metálico (pronto)'],
  obs=['O metal é orçado à parte.']),
 dict(id='resinas', title='Resinas foto e acrílica', items=[
  'Coroa total em resina Ceramage, com ou sem fibra',
  'Coroa total em resina popular, com ou sem fibra',
  'Coroa em acrílico',
  'Coroa provisória em acrílico',
  'Ponte fixa com fibra em resina Ceramage',
  'Ponte fixa com fibra em resina popular',
  'Ponte fixa com fibra acrílica',
  'Ponte provisória com fibra acrílica',
  'Restaurado em resina Ceramage, com ou sem fibra',
  'Restaurado em resina popular'],
  obs=['Consulte os tipos de resina disponíveis.']),
 dict(id='implantes', title='Implantes e protocolo', items=[
  'Barra de protocolo (até 4 elementos)',
  'Barra de protocolo (5 a 6 elementos)',
  'Barra clips (até 3 elementos)',
  'Guia cirúrgico',
  'Coroa metalocerâmica sobre implante'],
  obs=['Componentes e metais são orçados à parte.']),
 dict(id='ppr-roach', title='PPR (Roach)', items=[
  'Roach bilateral nacional com prensagem simples (pronta)',
  'Roach bilateral tipo Wisil com prensagem simples (pronta)',
  'Roach bilateral em Dental D (pronta)',
  'Roach bilateral em Flexidy (pronta)'],
  obs=['Nacional e tipo Wisil incluem metal, plano, montagem e prensagem.',
       'Dental D e Flexidy incluem metal, montagem e prensagem/aplicação.',
       'Em todas, os dentes são orçados à parte.']),
 dict(id='ppr-parcial', title='Parciais em acrílico e Flexite', items=[
  'Parcial simples (pronta)',
  'Parcial palato incolor (pronta)',
  'Parcial Coloform especial (pronta)',
  'Parcial dupla prensagem (pronta)',
  'Parcial Flexite unilateral (pronta)',
  'Parcial Flexite bilateral (pronta)'],
  obs=['Os dentes são orçados à parte.']),
 dict(id='ptr', title='Prótese total (PTR)', items=[
  'PTR simples (pronta)',
  'PTR palato incolor (pronta)',
  'PTR Coloform especial (pronta)',
  'PTR dupla prensagem (pronta)',
  'PTR STG – Sistema Tomas Gomes (pronta)'],
  obs=['Incluem chapa, montagem e prensagem.', 'Os dentes são orçados à parte.']),
 dict(id='placas', title='Placas, ortodontia e ortopedia', items=[
  'Placa de clareamento',
  'Placa de bruxismo cristal',
  'Placa de bruxismo emborrachada',
  'Placa de bruxismo em acrílico prensada',
  'Placa para esportes comuns',
  'Placa para luta',
  'Aparelho anti-ronco (Odonto Apneia)',
  'Aparelho ortodôntico móvel',
  'Contenção em fio',
  'Contenção estética (transparente)',
  'Contenção 3x3'],
  obs=['Confeccionamos todos os tipos e modelos de ortodontia e ortopedia.']),
]

# Condições gerais de trabalho (Tabela 2026 oficial, "Informações importantes"), sem valores.
CONDICOES = [
 'Todos os serviços são feitos sob orçamento, informado pelo WhatsApp ou pelo telefone.',
 'Dentes, soldas, componentes protéticos, ligas metálicas, vazamento, troquéis e gengivas artificiais são orçados à parte.',
 'O prazo médio de cada etapa do trabalho é de 7 dias úteis, podendo variar conforme a demanda.',
 'Trabalhos com urgência têm acréscimo de 30% em cada etapa. Consulte as condições.',
 'Recados e informações extras sobre o caso devem ser enviados por escrito junto com a requisição.',
 'Garantia de até 6 meses para defeito comprovado na confecção da peça, válida para serviços 100% realizados no laboratório.',
 'Trabalhos não iniciados ou não finalizados no laboratório não têm garantia.',
 'O pagamento deve ser feito até o dia 10 de cada mês.',
]
