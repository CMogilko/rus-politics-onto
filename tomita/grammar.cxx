#encoding "utf-8"    // сообщаем парсеру о том, в какой кодировке написана грамматика
#GRAMMAR_ROOT S      // указываем корневой нетерминал грамматики

// S -> Word<h-reg1, gram="anim">+;           // правило, выделяющее цепочку, состоящую из одного существительного
S -> Person interp (Politician.Who);
LName -> Word<gram="persn">;
FName -> Word<gram="famn">;
OName -> Word<gram="patrn">;
Person -> LName;
Person -> FName;
Person -> LName FName;
Person -> FName LName;
Person -> LName OName FName;
Person -> FName LName OName;
