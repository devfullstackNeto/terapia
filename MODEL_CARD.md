# Model Card — Engagement Forecast DEMO

**Banner:** NON-CLINICAL • DADOS SINTÉTICOS. Alvo: engajamento futuro no aplicativo. Modelos: maioria baseline, regressão logística e random forest, avaliados com validação cruzada estratificada de cinco folds e separação temporal entre features e alvo. Features: check-ins, uso de autocuidado, agendamentos e opt-in anteriores ao corte. Execução de 2026-09-29: baseline accuracy 0,500; regressão logística accuracy 0,696 / ROC-AUC 0,728; random forest accuracy 0,708 / ROC-AUC 0,774. Importâncias do random forest: check-ins 0,548; autocuidado 0,303; agendamentos 0,105; opt-in 0,044.

Uso proibido: diagnóstico, depressão, suicídio, risco clínico, decisão de cuidado ou perfil de pessoa real. Não integra nem é chamado pelo chat. Limites: dataset algorítmico, sem validade externa ou clínica; métricas são demonstrativas.
